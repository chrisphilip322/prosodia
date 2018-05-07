import functools
import typing

from .grammar import RuleName, Literal, RuleReference
from . import grammar as g
from .resolvable import (
    Resolvable,
    ResolvableFunc,
    ResolvablePair,
    resolve,
    resolve_map
)
from .tree import Node, RuleNode, LiteralNode
from ..validation.transform_validation import Validity, TypedFunc

I = typing.TypeVar('I')
O = typing.TypeVar('O')


class LanguageTransformation(object):
    def __init__(
        self,
        transformation_rules: typing.Dict[
            RuleName, 'RuleTransformation[typing.Any]'
        ]
    ) -> None:
        self.transformation_rules = transformation_rules

    @classmethod
    def create(cls) -> 'LanguageTransformation':
        return cls(dict())

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
            typing.Sequence[typing.Callable[[typing.Any], typing.Any]]
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
                'lang does not have the same set of rule names'
            )
        else:
            return sum(
                (
                    rule_t.validate(lang.rules[k], self)
                    for k, rule_t in self.transformation_rules.items()
                ),
                Validity.valid()
            )

    def get_transform_of_term(self, term: g.Term) -> typing.Callable:
        if isinstance(term, Literal):
            return LiteralNode.transform
        elif isinstance(term, RuleReference):
            return (
                self.transformation_rules[term.rule_name]
                    .tf_syntax.tf_term_groups[0].accumulator
            )
        else:
            raise ValueError


class RuleTransformation(typing.Generic[O]):
    def __init__(
        self,
        rule_name: RuleName,
        tf_syntax: 'SyntaxTransformation[O]'
    ) -> None:
        self.rule_name = rule_name
        self.tf_syntax = tf_syntax

    def transform(
        self,
        rule_node: RuleNode,
        lang: 'LanguageTransformation'
    ) -> Resolvable[O]:
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
                return validity + Validity.invalid(
                    '{0} rule is not valid'.format(repr(self.rule_name))
                )
            else:
                return Validity.valid()


class SyntaxTransformation(typing.Generic[O]):
    def __init__(
        self,
        tf_term_groups: typing.Sequence['TermGroupTransformation[O]']
    ) -> None:
        self.tf_term_groups = tf_term_groups

    @classmethod
    def create(
        cls,
        *tf_term_groups: 'TermGroupTransformation[O]'
    ) -> 'SyntaxTransformation':
        return cls(tf_term_groups)

    def transform(
        self,
        values: typing.Sequence[Node],
        index: int,
        lang: 'LanguageTransformation'
    ) -> Resolvable[O]:
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
                'the syntax has a different number of term groups than the'
                'transformation'
            )
        elif not TypedFunc.assert_substitutable(
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


class TermGroupTransformation(typing.Generic[O]):
    def __init__(
        self,
        accumulator: typing.Callable[[typing.Any], Resolvable[O]]
    ) -> None:
        self.accumulator = accumulator

    def transform(
        self,
        values: typing.Sequence[Node],
        lang: 'LanguageTransformation'
    ) -> Resolvable[O]:
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
        transforms = [
            lt.get_transform_of_term(term)
            for term in term_group.terms
        ]
        if not TypedFunc.assert_composable(transforms, self.accumulator):
            return Validity.invalid(
                'rule references in the term group are not composable',
                ' '.join(repr(t) for t in term_group.terms)
            )
        else:
            return Validity.valid()


@functools.singledispatch
def _lazy_getitem(_: typing.Any, __: typing.Any) -> typing.Any:
    raise NotImplementedError

@_lazy_getitem.register(int)
def _lazy_getitem_int(i: int, lazys: 'LazySequenceTransform') -> typing.Any:
    if i not in lazys.cache:
        lazys.cache[i] = lazys.initial_values[i].transform(lazys.lang)
    return lazys.cache[i]

@_lazy_getitem.register(slice)
def _lazy_getitem_slice(
    s: slice,
    lazys: 'LazySequenceTransform'
) -> typing.Sequence:
    return tuple(
        lazys[i]
        for i in range(len(lazys))[s]
    )


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
    def __getitem__(self, s: slice) -> typing.Sequence: # pylint: disable=function-redefined
        pass
    def __getitem__(self, x: typing.Union[int, slice]) -> typing.Any: # pylint: disable=function-redefined
        return _lazy_getitem(x, self)

    def __len__(self) -> int:
        return len(self.initial_values)

    def __iter__(self) -> typing.Iterator:
        return (self[i] for i in range(len(self)))
