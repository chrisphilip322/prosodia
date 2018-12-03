import typing

from .grammar import RuleName
from . import grammar as g
from .resolvable import (
    Resolvable,
    ResolvableFunc,
    ResolvablePair,
    resolve,
    resolve_map
)
from .tree import Node, RuleNode
from ..validation.validity import Validity
from ..validation.transform_validation import (
    check_composability, check_isomorphic)

InputType = typing.TypeVar('InputType')
OutputType = typing.TypeVar('OutputType')
T = typing.TypeVar('T')


class LanguageTransformation(typing.Generic[T]):
    def __init__(
        self,
        transformation_rules: typing.Dict[
            RuleName, 'RuleTransformation[typing.Any]'
        ],
        unused_root_rule: 'RuleTransformation[T]'
    ) -> None:
        self.transformation_rules = transformation_rules

    @classmethod
    def create(
        cls,
        rule_name: RuleName,
        root_accums: typing.Sequence[typing.Callable[..., T]]
    ) -> 'LanguageTransformation[T]':
        rt: RuleTransformation[T] = RuleTransformation(
            rule_name,
            SyntaxTransformation(
                tuple(
                    TermGroupTransformation(t) for t in typing.cast(
                        typing.Sequence[typing.Callable[..., Resolvable[T]]],
                        root_accums
                    )
                )
            )
        )
        return cls({rule_name: rt}, rt)

    def add_rule_transformation(
        self,
        rt: 'RuleTransformation'
    ) -> 'LanguageTransformation':
        self.transformation_rules[rt.rule_name] = rt
        return self

    def transform(self, node: Node) -> typing.Any:
        return resolve(node.transform(self))

    def __ilshift__(
        self,
        info: typing.Tuple[
            RuleName,
            typing.Sequence[typing.Callable[..., typing.Any]]
        ]
    ) -> 'LanguageTransformation':
        rule_name, transforms = info
        rt = RuleTransformation(
            rule_name,
            SyntaxTransformation(
                tuple(
                    TermGroupTransformation(t) for t in transforms
                )
            )
        )
        self.add_rule_transformation(rt)
        return self

    def validate(self, lang: g.Language) -> Validity:
        if self.transformation_rules.keys() != lang.rules.keys():
            return Validity.invalid(
                'lang does not have the same set of rule names. transform '
                'extras {0}, lang extras {1}.'.format(
                    self.transformation_rules.keys() - lang.rules.keys(),
                    lang.rules.keys() - self.transformation_rules.keys(),
                )
            )
        else:
            return sum(
                (
                    rule_t.validate(lang.rules[k], self)
                    for k, rule_t in self.transformation_rules.items()
                ),
                Validity.valid()
            )


class RuleTransformation(typing.Generic[OutputType]):
    def __init__(
        self,
        rule_name: RuleName,
        tf_syntax: 'SyntaxTransformation[OutputType]'
    ) -> None:
        self.rule_name = rule_name
        self.tf_syntax = tf_syntax

    def transform(
        self,
        rule_node: RuleNode,
        lang: 'LanguageTransformation'
    ) -> Resolvable[OutputType]:
        return ResolvableFunc(
            self.tf_syntax.transform,
            rule_node.children,
            rule_node.term_group_id,
            lang
        )

    def validate(
        self,
        rule: g.Rule,
        lt: 'LanguageTransformation'
    ) -> Validity:
        if self.rule_name != rule.name:
            return Validity.invalid(
                'rule transform is named differently than the rule'
            )
        else:
            validity = self.tf_syntax.validate(rule.syntax, lt)
            if not validity:
                v = validity + Validity.invalid(
                    '{0} rule is not valid'.format(repr(self.rule_name))
                )
                return v
            else:
                return Validity.valid()


class SyntaxTransformation(typing.Generic[OutputType]):
    def __init__(
        self,
        tf_term_groups: typing.Sequence['TermGroupTransformation[OutputType]']
    ) -> None:
        self.tf_term_groups = tf_term_groups

    @classmethod
    def create(
        cls,
        *tf_term_groups: 'TermGroupTransformation[OutputType]'
    ) -> 'SyntaxTransformation':
        return cls(tf_term_groups)

    def transform(
        self,
        values: typing.Sequence[Node],
        index: int,
        lang: 'LanguageTransformation'
    ) -> Resolvable[OutputType]:
        return ResolvableFunc(
            self.tf_term_groups[index].transform,
            values,
            lang
        )

    def validate(
        self,
        syntax: g.Syntax,
        lt: 'LanguageTransformation'
    ) -> Validity:
        if len(self.tf_term_groups) != len(syntax.term_groups):
            return Validity.invalid(
                'the syntax has a different number of term groups than the '
                'transformation. transform group count {0}, language group '
                'count {1}'.format(
                    len(self.tf_term_groups), len(syntax.term_groups)
                )
            )
        elif not check_isomorphic(
            tgt.accumulator for tgt in self.tf_term_groups
        ):
            return Validity.invalid(
                'not all term group transformations return the same type'
            )
        else:
            return sum(
                (
                    tgt.validate(tg, lt)
                    for tgt, tg in zip(self.tf_term_groups, syntax.term_groups)
                ),
                Validity.valid()
            )


class TermGroupTransformation(typing.Generic[OutputType]):
    def __init__(
        self,
        accumulator: typing.Callable[[typing.Any], Resolvable[OutputType]]
    ) -> None:
        self.accumulator = accumulator

    def transform(
        self,
        values: typing.Sequence[Node],
        lang: 'LanguageTransformation'
    ) -> Resolvable[OutputType]:
        return ResolvablePair(
            resolve_map(
                values,
                lambda v: v.transform(lang)
            ),
            self.accumulator
        )

    def validate(
        self,
        term_group: g.TermGroup,
        lt: 'LanguageTransformation'
    ) -> Validity:
        transform_types = [
            term.get_transform_type(lt)
            for term in term_group.terms
        ]
        is_composable = check_composability(transform_types, self.accumulator)
        if not is_composable:
            return is_composable + Validity.invalid(
                'rule references in the term group are not composable: '
                + ' '.join(repr(t) for t in term_group.terms)
            )
        else:
            return Validity.valid()


class LazySequenceTransform(typing.Sequence):
    def __init__(
        self,
        initial_values: typing.Sequence[Node],
        lang: 'LanguageTransformation',
        cache: typing.Dict[int, typing.Any]
    ) -> None:
        super().__init__()
        self.initial_values = initial_values
        self.lang = lang
        self.cache = cache

    @classmethod
    def create(
        cls,
        nodes: typing.Sequence[Node],
        lang: 'LanguageTransformation'
    ) -> 'LazySequenceTransform':
        return cls(nodes, lang, dict())

    @typing.overload
    def __getitem__(self, i: int) -> typing.Any:
        pass

    @typing.overload
    def __getitem__(self, s: slice) -> typing.Sequence:  # pylint: disable=function-redefined
        pass

    def __getitem__(self, x: typing.Union[int, slice]) -> typing.Any:\
            # pylint: disable=function-redefined
        if isinstance(x, int):
            if x not in self.cache:
                self.cache[x] = self.initial_values[x].transform(self.lang)
            return self.cache[x]
        elif isinstance(x, slice):
            return tuple(
                self[i]
                for i in range(len(self))[x]
            )
        else:
            raise TypeError(
                'Expected `x` to be a Union[int, slice] but got {0}'.format(
                    type(x)
                )
            )

    def __len__(self) -> int:
        return len(self.initial_values)

    def __iter__(self) -> typing.Iterator:
        return (self[i] for i in range(len(self)))
