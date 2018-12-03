import abc
from functools import partial
import typing

from .tree import Node, LiteralNode, RuleNode, MultiNode
from ..validation.validity import Validity
from ..validation import group_types as gt
from ..validation.transform_validation import get_return_type
if typing.TYPE_CHECKING:
    from .transform import LanguageTransformation  # pylint: disable=unused-import

RuleName = str
MatchResult = typing.Tuple['_SmartText', Node]
T = typing.TypeVar('T')


class Grammar(typing.Generic[T]):
    def __init__(
        self,
        language: 'Language',
        transform: 'LanguageTransformation[T]',
        allow_partial_matches: bool = True
    ) -> None:
        self.language = language
        self.transform = transform
        self.allow_partial_matches = allow_partial_matches

    def apply(self, text: str) -> T:
        return self.transform.transform(
            self.language.parse(
                text,
                self.allow_partial_matches
            )
        )

    def validate(self) -> Validity:
        return self.language.validate() + self.transform.validate(self.language)


class _SmartText(object):
    __slots__ = ['_raw_text', '_start', '_end']

    def __init__(
        self,
        raw_text: str,
        *,
        _start: int = None,
        _end: int = None
    ) -> None:
        self._raw_text = raw_text
        self._start = 0 if _start is None else _start
        self._end = len(raw_text) if _end is None else _end

    def __len__(self) -> int:
        return self._end - self._start

    def log_front(self, size: int, *args: object) -> None:
        segment = self._raw_text[
            self._start:self._end if len(self) < size else self._start + size
        ]
        print(len(self), self._start, self._end, repr(segment), *args)

    def startswith(self, target: str, case_sensitive: bool = True) -> bool:
        src = self._raw_text[self._start: self._start + len(target)]
        if case_sensitive:
            return src == target
        else:
            return src.lower() == target.lower()

    @typing.overload
    def __getitem__(self, index: int) -> str:
        pass

    @typing.overload
    def __getitem__(self, index: slice) -> '_SmartText':  # pylint: disable=function-redefined
        pass

    def __getitem__(self, index: typing.Any) -> typing.Any:  # pylint: disable=function-redefined
        if isinstance(index, int):
            return self._raw_text[self._start + index]
        elif isinstance(index, slice):
            if index.step is not None and index.step != 1:
                raise TypeError('cannot use step of not 1 with _SmartText')
            start = self._start + (index.start or 0)
            if index.stop is None:
                end = self._end
            else:
                end = start + index.stop
            return _SmartText(self._raw_text, _start=start, _end=end)
        else:
            raise TypeError('expecting an int or a slice')


class NoMatches(Exception):
    pass


class TooManyMatches(Exception):
    def __init__(self, matches: typing.Sequence[Node]) -> None:
        super().__init__(self)
        self.matches = matches


class Language(object):
    """Collection of rules"""
    def __init__(
        self,
        rules: typing.Dict[RuleName, 'Rule'],
        root_rule: RuleName,
        debug: bool = False
    ) -> None:
        self.rules = rules
        self.root_rule = root_rule
        self.debug = debug

    @classmethod
    def create(cls, root_rule: RuleName) -> 'Language':
        return cls(dict(), root_rule)

    def log_match(self, text: _SmartText, *args: object) -> None:
        if self.debug:
            text.log_front(20, *args)

    def add_rule(self, rule: 'Rule') -> 'Language':
        if rule.name in self.rules:
            raise ValueError(
                'Rule with that name is already in this Language: {0}'.format(
                    rule.name
                )
            )
        self.rules[rule.name] = rule
        return self

    def get_rule(self, rule_name: RuleName) -> 'Rule':
        return self.rules[rule_name]

    def add_to_rule(
        self,
        rule_name: RuleName,
        tgs: typing.Sequence['TermGroup']
    ) -> None:
        self.rules[rule_name].syntax.term_groups = (
            list(self.rules[rule_name].syntax.term_groups) + list(tgs)
        )

    def parse(self, raw_text: str, allow_partial_matches: bool = True) -> Node:
        text = _SmartText(raw_text)
        matches = tuple(self._parse_all(text, allow_partial_matches))
        if not matches:
            raise NoMatches
        elif len(matches) > 1:
            for m in matches:
                print(m.draw())
            raise TooManyMatches(matches)
        else:
            return matches[0]

    def _parse_all(
        self,
        text: _SmartText,
        allow_partial_matches: bool
    ) -> typing.Iterable[Node]:
        root = self.get_rule(self.root_rule)
        matches = root.match(text, self)
        for leftover, node in matches:
            if allow_partial_matches or not leftover:
                yield node

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
        text: _SmartText,
        lang: 'Language'
    ) -> typing.Iterable[MatchResult]:
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
        text: _SmartText,
        rule_name: 'RuleName',
        lang: 'Language'
    ) -> typing.Iterable[MatchResult]:
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
        text: _SmartText,
        term_index: int,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[_SmartText, typing.Sequence[Node]]]:
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
        text: _SmartText,
        lang: 'Language'
    ) -> typing.Iterable[typing.Tuple[_SmartText, typing.Sequence[Node]]]:
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
            len(self.terms) > 1
            and any(t.equals(Literal('')) for t in self.terms)
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
        text: _SmartText,
        lang: 'Language'
    ) -> typing.Iterable[MatchResult]:
        raise NotImplementedError

    @abc.abstractmethod
    def validate(self, lang: 'Language') -> Validity:
        raise NotImplementedError

    @abc.abstractmethod
    def equals(self, other: 'Term') -> Validity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        raise NotImplementedError


class RuleReference(Term):
    """Term that represents a nested rule"""
    def __init__(self, rule_name: RuleName) -> None:
        self.rule_name = rule_name

    def match(
        self,
        text: _SmartText,
        lang: 'Language'
    ) -> typing.Iterable[MatchResult]:
        matches = lang.get_rule(self.rule_name).match(text, lang)
        for match in matches:
            lang.log_match(match[0], 'rule ref', self.rule_name)
            yield match

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
                'rule reference points to a rule that does not exist: {0!r}'
                .format(self.rule_name)
            )
        else:
            return Validity.valid()

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        rules = lt.transformation_rules
        return get_return_type(
            rules[self.rule_name].tf_syntax.tf_term_groups[0].accumulator
        )


class Literal(Term):
    """Term that represents a plaintext literal"""
    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        self.text = text
        self.case_sensitive = case_sensitive

    def match(
        self,
        text: _SmartText,
        lang: Language
    ) -> typing.Iterable[MatchResult]:
        if text.startswith(self.text, self.case_sensitive):
            lang.log_match(text, 'literal', self.text)
            yield text[len(self.text):], LiteralNode(self.text)

    def __repr__(self) -> str:
        return '<Literal(Term) {0!r}>'.format(self.text)

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, Literal):
            return Validity.invalid('Literal: other is not a literal')
        elif self.text != other.text:
            return Validity.invalid('Literal: text is different')
        else:
            return Validity.valid()

    def validate(self, lang: Language) -> Validity:
        return Validity.valid()

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        return get_return_type(LiteralNode.transform)


class LiteralRange(Term):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def match(
        self,
        text: _SmartText,
        lang: Language
    ) -> typing.Iterable[MatchResult]:
        if text:
            first_char = text[0]
            if self.min_value <= ord(first_char) <= self.max_value:
                lang.log_match(text, 'range', self.min_value, self.max_value)
                yield text[1:], LiteralNode(first_char)

    def __repr__(self) -> str:
        return '<LiteralRange(Term) {0}, {1}>'.format(
            self.min_value,
            self.max_value
        )

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, LiteralRange):
            return Validity.invalid(
                'LiteralRange: other is not a literal range'
            )
        elif (
            self.min_value != other.min_value
            or self.max_value != other.max_value
        ):
            return Validity.invalid('LiteralRange: range values are different')
        else:
            return Validity.valid()

    def validate(self, lang: Language) -> Validity:
        if self.max_value < self.min_value:
            return Validity.invalid('LiteralRange: max cannot be less than min')
        elif self.max_value < 0 or self.min_value < 0:
            return Validity.invalid(
                'LiteralRange: cannot have negative range values'
            )
        else:
            return Validity.valid()

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        return get_return_type(LiteralNode.transform)


class EOFTerm(Term):
    def match(
        self,
        text: _SmartText,
        lang: 'Language'
    ) -> typing.Iterable[MatchResult]:
        if not text:
            lang.log_match(text, 'EOF')
            yield text, LiteralNode('')

    def __repr__(self) -> str:
        return '<EOFTerm(Term)>'

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, EOFTerm):
            return Validity.invalid('EOFTerm: other is not an EOFTerm')
        else:
            return Validity.valid()

    def validate(self, lang: Language) -> Validity:
        return Validity.valid()

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        return get_return_type(LiteralNode.transform)


class RepeatTerm(Term):
    def __init__(
        self,
        child: Term,
        min_count: int,
        max_count: typing.Optional[int]
    ) -> None:
        self.child = child
        self.min_count = min_count
        self.max_count = max_count

    def __repr__(self) -> str:
        return '<RepeatTerm(Term) {0!r},{1},{2}>'.format(
            self.child,
            self.min_count,
            self.max_count
        )

    def match(
        self,
        text: _SmartText,
        lang: Language
    ) -> typing.Iterable[MatchResult]:
        match, more_funcs = self._match_impl(
            text,
            lang,
            []
        )
        if match:
            yield match
        for func in more_funcs:
            match, even_more_funcs = func()
            if match:
                lang.log_match(match[0], 'repeat', len(match[1].children))
                yield match
            more_funcs += even_more_funcs

    def _match_impl(
        self,
        text: _SmartText,
        lang: Language,
        matched_terms: typing.Sequence[Node]
    ) -> typing.Tuple[
        typing.Optional[typing.Tuple[_SmartText, MultiNode]],
        typing.Iterable[typing.Callable[[], typing.Any]]
    ]:
        if self.max_count is not None and len(matched_terms) > self.max_count:
            return None, []
        if len(matched_terms) >= self.min_count:
            match: typing.Optional[typing.Tuple[_SmartText, MultiNode]] = (
                text, MultiNode(matched_terms)
            )
        else:
            match = None

        more_funcs = [
            partial(
                self._match_impl,
                leftover_text,
                lang,
                list(matched_terms) + [term]
            ) for leftover_text, term in self.child.match(text, lang)
        ]
        return match, more_funcs

    def equals(self, other: Term) -> Validity:
        if not isinstance(other, RepeatTerm):
            return Validity.invalid('RepeatTerm: other is not a RepeatTerm')
        elif (
            self.min_count != other.min_count
            or self.max_count != other.max_count
        ):
            return Validity.invalid(
                'RepeatTerm: other does not have same range'
            )
        validity = self.child.equals(other.child)
        if not validity:
            return validity + Validity.invalid(
                'RepeatTerm: children are not equal'
            )
        else:
            return Validity.valid()

    def validate(self, lang: Language) -> Validity:
        if (
            self.max_count is not None
            and self.max_count < self.min_count
        ):
            return Validity.invalid(
                'RepeatTerm: max count is less than min count'
            )
        elif self.max_count is not None and self.max_count < 0:
            return Validity.invalid(
                'RepeatTerm: max count cannot be negative'
            )
        elif self.min_count < 0:
            return Validity.invalid(
                'RepeatTerm: min count cannot be negative'
            )
        validity = self.child.validate(lang)
        if not validity:
            return validity + Validity.invalid(
                'RepeatTerm: child is not valid'
            )
        else:
            return Validity.valid()

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:
        return typing.Sequence[self.child.get_transform_type(lt)]  # type: ignore


class GroupTerm(Term):
    def __init__(
        self,
        children_groups: typing.Sequence[typing.Sequence[Term]]
    ) -> None:
        self.children_groups = children_groups

    def __repr__(self) -> str:
        return '<GroupTerm(Term) {0}>'.format(
            ','.join(
                '({0})'.format(
                    ','.join(repr(c) for c in children)
                ) for children in self.children_groups
            )
        )

    def equals(self, other: object) -> Validity:
        if not isinstance(other, GroupTerm):
            return Validity.invalid(
                'GroupTerm: other is not a GroupTerm'
            )
        elif len(self.children_groups) != len(other.children_groups):
            return Validity.invalid(
                'GroupTerm: this term has {0} children_groups and other has {1} '
                'children_groups'.format(
                    len(self.children_groups), len(other.children_groups)
                )
            )
        validity = Validity.valid()
        for index, (a, b) in enumerate(
            zip(self.children_groups, other.children_groups)
        ):
            if len(a) != len(b):
                validity += Validity.invalid(
                    'GroupTerm: children_groups {0} are not the same length'
                    .format(index)
                )
            else:
                validity += sum(
                    (c.equals(o) for c, o in zip(a, b)),
                    Validity.valid()
                )
        return validity

    def match(
        self,
        text: _SmartText,
        lang: Language
    ) -> typing.Iterable[MatchResult]:
        for index, children in enumerate(self.children_groups):
            for leftover, match in _group_match(children, text, lang):
                yield leftover, MultiNode(match, (index, len(self.children_groups)))

    def validate(self, lang: Language) -> Validity:
        # TODO: validate if the grouping term is necessary, but requires extra context
        if len(self.children_groups) <= 1 and len(self.children_groups[0]) <= 1:
            return Validity.invalid(
                'GroupTerm: must have at least two children'
            )
        children = [
            c.validate(lang)
            for children in self.children_groups
            for c in children
        ]
        if all(children):
            return Validity.valid()
        else:
            msg_groups = [
                list(c.messages) + [
                    'GroupTerm[{0}]: invalid child'.format(index)
                ]
                for index, c in enumerate(children) if not c
            ]
            return (
                Validity(
                    [msg for group in msg_groups for msg in group]
                ) + Validity.invalid('GroupTerm: children are not valid')
            )

    def get_transform_type(self, lt: 'LanguageTransformation') -> type:  # pylint: disable=too-many-return-statements,too-many-branches
        child_types = tuple(
            typing.Tuple[tuple(
                c.get_transform_type(lt) for c in children
            )] for children in self.children_groups
        )
        # c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15 = \
        #     itertools.islice(
        #         itertools.chain(child_types_gen, itertools.repeat(None))
        #         16
        #     )
        if len(self.children_groups) == 1:
            return gt.Group[child_types]  # type: ignore
        elif len(self.children_groups) == 2:
            return gt.Group2[child_types]  # type: ignore
        elif len(self.children_groups) == 3:
            return gt.Group3[child_types]  # type: ignore
        elif len(self.children_groups) == 4:
            return gt.Group4[child_types]  # type: ignore
        elif len(self.children_groups) == 5:
            return gt.Group5[child_types]  # type: ignore
        elif len(self.children_groups) == 6:
            return gt.Group6[child_types]  # type: ignore
        elif len(self.children_groups) == 7:
            return gt.Group7[child_types]  # type: ignore
        elif len(self.children_groups) == 8:
            return gt.Group8[child_types]  # type: ignore
        elif len(self.children_groups) == 9:
            return gt.Group9[child_types]  # type: ignore
        elif len(self.children_groups) == 10:
            return gt.Group10[child_types]  # type: ignore
        elif len(self.children_groups) == 11:
            return gt.Group11[child_types]  # type: ignore
        elif len(self.children_groups) == 12:
            return gt.Group12[child_types]  # type: ignore
        elif len(self.children_groups) == 13:
            return gt.Group13[child_types]  # type: ignore
        elif len(self.children_groups) == 14:
            return gt.Group14[child_types]  # type: ignore
        elif len(self.children_groups) == 15:
            return gt.Group15[child_types]  # type: ignore
        elif len(self.children_groups) == 16:
            return gt.Group16[child_types]  # type: ignore
        else:
            raise ValueError('cant have more than 16 child groups')


def _group_match(
    children: typing.Sequence[Term],
    text: _SmartText,
    lang: Language
) -> typing.Iterable[typing.Tuple[_SmartText, typing.Sequence[Node]]]:
    funcs: typing.List[typing.Callable[[], typing.Any]] = [
        partial(_group_match_impl, children, text, lang, [])
    ]
    for f in funcs:
        result: typing.Union[
            typing.Tuple[_SmartText, typing.Sequence[Node]],
            typing.List[typing.Callable[[], typing.Any]]
        ] = f()
        if isinstance(result, tuple):
            yield result
        else:
            funcs += result


def _group_match_impl(
    children: typing.Sequence[Term],
    text: _SmartText,
    lang: Language,
    matched_terms: typing.Sequence[Node]
) -> typing.Union[
    typing.Tuple[_SmartText, typing.Sequence[Node]],
    typing.List[typing.Callable[[], typing.Any]]
]:
    if len(matched_terms) == len(children):
        return text, matched_terms
    else:
        target = children[len(matched_terms)]
        return [
            partial(
                _group_match_impl,
                children,
                leftover,
                lang,
                list(matched_terms) + [node]
            ) for leftover, node in target.match(text, lang)
        ]
