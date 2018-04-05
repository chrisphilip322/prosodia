import functools
import typing

from .grammar import RuleName
from .tree import Node, RuleNode

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
    def create(cls):
        return cls(dict())

    def add_rule_transformation(
        self,
        rt: 'RuleTransformation'
    ) -> 'LanguageTransformation':
        self.transformation_rules[rt.rule_name] = rt
        return self

    def transform(self, rule_node: RuleNode) -> typing.Any:
        return rule_node.transform(self)

    def __ilshift__(
        self,
        info: typing.Tuple[
            RuleName,
            typing.Sequence[typing.Callable[[typing.Any], O]]
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
        rule_node: 'RuleNode',
        lang: 'LanguageTransformation'
    ) -> O:
        return self.tf_syntax.transform(
            rule_node.children,
            rule_node.term_group_id,
            lang
        )


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
    ) -> O:
        return self.tf_term_groups[index].transform(values, lang)


class TermGroupTransformation(typing.Generic[O]):
    def __init__(
        self,
        accumulator: typing.Callable[[typing.Any], O]
    ) -> None:
        self.accumulator = accumulator

    def transform(
        self,
        values: typing.Sequence[Node],
        lang: 'LanguageTransformation'
    ) -> O:
        return self.accumulator(
            LazySequenceTransform.create(
                values,
                lang
            )
        )


@functools.singledispatch
def _lazy_getitem(_, __):
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
        initial_values: typing.Sequence['Node'],
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
        nodes: typing.Sequence['Node'],
        lang: 'LanguageTransformation'
    ) -> 'LazySequenceTransform':
        return cls(nodes, lang, dict())

    @typing.overload
    def __getitem__(self, i: int) -> typing.Any:
        pass
    @typing.overload
    def __getitem__(self, s: slice) -> typing.Sequence: # pylint: disable=function-redefined
        pass
    def __getitem__(self, x): # pylint: disable=function-redefined
        return _lazy_getitem(x, self)

    def __len__(self):
        return len(self.initial_values)

    def __iter__(self):
        return (self[i] for i in range(len(self)))
