import abc
import re
import typing

from .resolvable import resolve_map, ResolvablePair, ResolvableFunc, Resolvable
from ..validation import group_types as gt

if typing.TYPE_CHECKING:
    from .transform import LanguageTransformation  # pylint: disable=unused-import

RE_LINE_START = re.compile('^', flags=re.MULTILINE)
RuleName = str


class Node(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def transform(self, lang: 'LanguageTransformation') -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def draw(self) -> str:
        raise NotImplementedError


class RuleNode(Node):
    def __init__(
        self,
        matched_rule: RuleName,
        term_group_id: int,
        children: typing.Sequence[Node]
    ) -> None:
        self.matched_rule = matched_rule
        self.term_group_id = term_group_id
        self.children = children

    def __str__(self) -> str:
        return ''.join(str(c) for c in self.children)

    def __repr__(self) -> str:
        return '<RuleNode {0}>'.format(repr(self.matched_rule))

    def transform(self, lang: 'LanguageTransformation') -> typing.Any:
        return lang.transformation_rules[self.matched_rule].transform(
            self,
            lang
        )

    def draw(self) -> str:
        children = (
            RE_LINE_START.sub('  ', child.draw()) for child in self.children
        )
        return '\n'.join(
            [
                repr(self),
                *children
            ]
        )


class LiteralNode(Node):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return '<LiteralNode {0}>'.format(repr(self.value))

    def transform(self, lang: 'LanguageTransformation') -> str:
        return self.value

    def draw(self) -> str:
        return repr(self)


class MultiNode(Node):
    def __init__(
        self,
        children: typing.Sequence[Node],
        group_info: typing.Optional[typing.Tuple[int, int]] = None,
    ) -> None:
        self.children = children
        self.group_info = group_info
        # group_info[0] index of the group that matched
        # group_info[1] total number of groups

    def transform(self, lang: 'LanguageTransformation') -> typing.Any:
        resolvable_result = resolve_map(
            self.children,
            lambda c: c.transform(lang)
        )
        if self.group_info is None:
            return resolvable_result
        else:
            return self._make_group_result(
                resolvable_result
            )

    def __str__(self) -> str:
        return ''.join(str(child) for child in self.children)

    def __repr__(self) -> str:
        if not self.children:
            return '<MultiNode 0>'
        else:
            return '<MultiNode {0}>'.format(
                ','.join(repr(c) for c in self.children)
            )

    def draw(self) -> str:
        children = (
            RE_LINE_START.sub('  ', child.draw()) for child in self.children
        )
        return '\n'.join(
            [
                repr(self),
                *children
            ]
        )

    def _make_group_result(self, resolvable: Resolvable) -> Resolvable:
        def func(result: typing.Any) -> Resolvable:
            def nested() -> typing.Any:
                if self.group_info:
                    output = [gt.NoValue.Sentinel] * self.group_info[1]
                    output[self.group_info[0]] = result
                    return output
                else:
                    raise RuntimeError

            return ResolvableFunc(nested)

        return ResolvablePair(resolvable, func)
