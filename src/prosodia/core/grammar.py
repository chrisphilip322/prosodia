import abc
import typing

from .tree import Node, LiteralNode, RuleNode
from ..validation.transform_validation import Validity

RuleName = str


class Language(object):
    """Collection of rules"""
    def __init__(
        self,
        rules: typing.Dict[RuleName, 'Rule'],
        root_rule: RuleName
    ) -> None:
        self.rules = rules
        self.root_rule = root_rule

    @classmethod
    def create(cls, root_rule: RuleName) -> 'Language':
        return cls(dict(), root_rule)

    def add_rule(self, rule: 'Rule') -> 'Language':
        if rule.name in self.rules:
            raise ValueError('Rule with that name is already in this Language')
        self.rules[rule.name] = rule
        return self

    def get_rule(self, rule_name: RuleName) -> 'Rule':
        return self.rules[rule_name]

    def parse(self, text: str) -> Node:
        matches = self._parse_all(text)
        node, = matches
        return node

    def _parse_all(self, text: str) -> typing.Iterable[Node]:
        root = self.get_rule(self.root_rule)
        matches = root.match(text, self)
        return (node for _, node in matches)

    def equals(self, other: 'Language') -> Validity:
        if self.root_rule != other.root_rule:
            return Validity.invalid('Langage: root rule is different')
        elif self.rules.keys() != other.rules.keys():
            return Validity.invalid('Language: set of rule names are different')

        validity = sum(
            (
                r.equals(other.rules[k])
                for k, r in self.rules.items()
            ),
            Validity.valid()
        )
        if not validity:
            return validity + Validity.invalid('Language: rules are different')
        else:
            return Validity.valid()

    def validate(self) -> Validity:
        if self.root_rule not in self.rules:
            return Validity.invalid('root rule is not present in language')
        else:
            return sum(
                (
                    rule.validate(self)
                    for rule in self.rules.values()
                ),
                Validity.valid()
            )


class Rule(object):
    """Syntax rule

    each transformation in the map must match the format of the syntax
    """
    def __init__(
        self,
        name: RuleName,
        syntax: 'Syntax'
    ) -> None:
        self.name = name
        self.syntax = syntax

    def match(
        self,
        text: str,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        return self.syntax.match(text, self.name, lang)

    def equals(self, other: 'Rule') -> Validity:
        if self.name != other.name:
            return Validity.invalid('Rule: rule names are different')

        validity = self.syntax.equals(other.syntax)
        if not validity:
            return validity + Validity.invalid('Rule: syntaxes are different')
        else:
            return Validity.valid()

    def validate(self, lang: 'Language') -> Validity:
        return self.syntax.validate(self.name, lang)


class Syntax(object):
    """Collection of Term lists

    a syntax matches if one of its term lists matches the plaintext
    """
    def __init__(self, term_groups: typing.Sequence['TermGroup']) -> None:
        self.term_groups = term_groups

    @classmethod
    def create(cls, *term_groups: 'TermGroup') -> 'Syntax':
        return cls(term_groups)

    def match(
        self,
        text: str,
        rule_name: 'RuleName',
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        for index, term_list in enumerate(self.term_groups):
            for leftover, terms in term_list.match(text, lang):
                node = RuleNode(rule_name, index, terms)
                yield leftover, node


    def equals(self, other: 'Syntax') -> Validity:
        if len(self.term_groups) != len(other.term_groups):
            return Validity.invalid(
                'Syntax: number of term groups are different'
            )
        validity = sum(
            (
                i.equals(j)
                for i, j in zip(self.term_groups, other.term_groups)
            ),
            Validity.valid()
        )
        if not validity:
            return validity + Validity.invalid(
                'Syntax: term groups are different'
            )
        else:
            return Validity.valid()

    def validate(self, rule_name: RuleName, lang: 'Language') -> Validity:
        dupes = tuple(
            (i, j, x)
            for i, x in enumerate(self.term_groups)
            for j, y in enumerate(self.term_groups)
            if i != j and x.equals(y)
        )
        if dupes:
            return Validity.invalid('syntax has duplicate term groups')
        else:
            return sum(
                (tg.validate(rule_name, lang) for tg in self.term_groups),
                Validity.valid()
            )


class TermGroup(object):
    """Collection of Terms"""
    def __init__(self, terms: typing.Sequence['Term']) -> None:
        self.terms = terms

    @classmethod
    def create(cls, *terms: 'Term') -> 'TermGroup':
        return cls(terms)

    def _match_impl(
        self,
        text: str,
        term_index: int,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, typing.Sequence[Node]]]:
        term = self.terms[term_index]
        next_term_index = term_index + 1
        is_last_term = next_term_index >= len(self.terms)
        for leftover, match in term.match(text, lang):
            if is_last_term:
                yield leftover, (match,)
            else:
                for final_leftover, child_matches in self._match_impl(
                    leftover,
                    next_term_index,
                    lang
                ):
                    yield final_leftover, (match,) + tuple(child_matches)

    def match(
        self,
        text: str,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, typing.Sequence[Node]]]:
        return self._match_impl(text, 0, lang)

    def equals(self, other: 'TermGroup') -> Validity:
        if len(self.terms) != len(other.terms):
            return Validity.invalid(
                'TermGroup: number of terms are different'
            )
        validity = sum(
            (
                i.equals(j)
                for i, j in zip(self.terms, other.terms)
            ),
            Validity.valid()
        )
        if not validity:
            return validity + Validity.invalid(
                'TermGroup: terms are different'
            )
        else:
            return Validity.valid()

    def validate(self, rule_name: RuleName, lang: 'Language') -> Validity:
        if not self.terms:
            return Validity.invalid(
                'term group needs at least one term'
            )
        elif (
            len(self.terms) > 1 and
            any(t.equals(Literal('')) for t in self.terms)
        ):
            return Validity.invalid(
                'shouldnt have an empty literal in a term group with more than '
                'one term'
            )
        elif self.terms[0].equals(RuleReference(rule_name)):
            return Validity.invalid(
                'term group cannot start with its own rule'
            )
        else:
            return sum(
                (t.validate(lang) for t in self.terms),
                Validity.valid()
            )


class Term(object, metaclass=abc.ABCMeta):
    """Unit of a syntax"""
    @abc.abstractmethod
    def match(
        self,
        text: str,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        raise NotImplementedError

    def validate(self, _: 'Language') -> Validity:  # pylint: disable=no-self-use
        return Validity.valid()

    @abc.abstractmethod
    def equals(self, other: 'Term') -> Validity:
        raise NotImplementedError


class RuleReference(Term):
    """Term that represents a nested rule"""
    def __init__(self, rule_name: RuleName) -> None:
        self.rule_name = rule_name

    def match(
        self,
        text: str,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        return lang.get_rule(self.rule_name).match(text, lang)

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, RuleReference):
            return Validity.invalid(
                'RuleReference: other is not rule reference'
            )
        elif self.rule_name != other.rule_name:
            return Validity.invalid('RuleReference: different rule names')
        else:
            return Validity.valid()

    def __repr__(self) -> str:
        return '<RuleReference(Term) {0}>'.format(self.rule_name)

    def validate(self, lang: 'Language') -> Validity:
        if self.rule_name not in lang.rules:
            return Validity.invalid(
                'rule reference points to a rule that does not exist'
            )
        else:
            return Validity.valid()

class Literal(Term):
    """Term that represents a plaintext literal"""
    def __init__(self, text: str) -> None:
        self.text = text

    def match(
        self,
        text: str,
        lang: Language
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        if text.startswith(self.text):
            yield text[len(self.text):], LiteralNode(self.text)

    def __repr__(self) -> str:
        return '<Literal(Term) {0}>'.format(self.text)

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, Literal):
            return Validity.invalid('Literal: other is not a literal')
        elif self.text != other.text:
            return Validity.invalid('Literal: text is different')
        else:
            return Validity.valid()


class EOFTerm(Literal):
    def __init__(self) -> None:
        super().__init__('')

    def match(
        self,
        text: str,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[str, Node]]:
        if text == '':
            yield text, LiteralNode('')

    def __repr__(self) -> str:
        return '<EOFTerm(Term)>'

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, EOFTerm):
            return Validity.invalid('EOFTerm: other is not an EOFTerm')
        else:
            return Validity.valid()
