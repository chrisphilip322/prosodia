import abc
import typing

if typing.TYPE_CHECKING:
    from .grammar import RuleName
    from .transform import LanguageTransformation


class Node(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def transform(self, lang: 'LanguageTransformation') -> typing.Any:
        raise NotImplementedError


class RuleNode(Node):
    def __init__(
        self,
        matched_rule: 'RuleName',
        term_group_id: int,
        children: typing.Sequence[Node]
    ) -> None:
        self.matched_rule = matched_rule
        self.term_group_id = term_group_id
        self.children = children

    def __str__(self):
        return ''.join(str(c) for c in self.children)

    def transform(self, lang: 'LanguageTransformation') -> typing.Any:
        return lang.transformation_rules[self.matched_rule].transform(
            self,
            lang
        )


class LiteralNode(Node):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self):
        return self.value

    def transform(self, lang: 'LanguageTransformation') -> str:
        return self.value
