import abc
import re
import typing

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
