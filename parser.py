#!/usr/bin/env python

import types
from itertools import count
import os

LOGGING_ENABLED = os.getenv('DEBUG')

uniqs = count()
def log(func):
    def wrapped(*args):
        my_uniq = next(uniqs)
        if LOGGING_ENABLED:
            print(
                "{:05d}s".format(my_uniq),
                func.__name__,
                *(repr(x) for x in args)
            )
        result = func(*args)
        if isinstance(result, types.GeneratorType):
            def uberwrapped(result):
                yield from result
                if LOGGING_ENABLED:
                    print(
                        "{:05d}e".format(my_uniq),
                        func.__name__,
                        *(repr(x) for x in args)
                    )
            result = uberwrapped(result)
        else:
            if LOGGING_ENABLED:
                print(
                    "{:05d}e".format(my_uniq),
                    func.__name__,
                    *(repr(x) for x in args)
                )
        return result
    return wrapped


def parse(text, expressions):
    expr, *rest = expressions
    if isinstance(expr, str):
        matches = parse_string(text, expr)
    else:
        matches = expr.match(text)
    for leftover, match in matches:
        if rest:
            for final_leftover, child_matches in parse(leftover, rest):
                yield final_leftover, (match,) + child_matches
        else:
            yield leftover, (match,)


def parse_string(text, string):
    if text.startswith(string):
        yield text[len(string):], string


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class BNF(object):
    def __init__(self, value, expression_num):
        self.value = value
        self.expression_num = expression_num

    @classproperty
    def syntax(self):
        raise NotImplementedError

    def __str__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            self.value
        )

    def print(self, depth=0):
        print(' '*depth+self.__class__.__name__)
        for v in self.value:
            if isinstance(v, BNF):
                v.print(depth+1)
            else:
                print(' '*(depth+1)+repr(v))

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            len(self.value) == len(other.value) and
            all(a == b for a, b in zip(self.value, other.value))
        )

    @classmethod
    def match(cls, text):
        for expression_num, expressions in enumerate(cls.syntax):
            for leftover, children in parse(text, expressions):
                obj = cls(children, expression_num)
                yield leftover, obj


class Syntax(BNF):
    @classproperty
    def syntax(self):
        return (
            (Rules, EndOfFile,),
        )

    def as_syntax(self):
        return self.value[0].as_syntax()


class Rules(BNF):
    @classproperty
    def syntax(self):
        return (
            (Rule,),
            (Rule, Rules),
        )

    def as_syntax(self):
        value = (self.value[0].as_syntax(),)
        if len(self.value) == 1:
            return value
        else:
            return value + self.value[1].as_syntax()


class EndOfFile(BNF):
    @classmethod
    def match(cls, text):
        if text == '':
            yield (text, cls(tuple(), 0),)

    syntax = None


class Rule(BNF):
    @classproperty
    def syntax(self):
        return (
            (
                OptWhitespace, '<', RuleName, '>', OptWhitespace, '::=',
                OptWhitespace, Expression, LineEnd
            ),
        )

    def as_syntax(self):
        return (self.value[2].as_syntax(), self.value[7].as_syntax())


class OptWhitespace(BNF):
    @classproperty
    def syntax(self):
        return (
            (" ", OptWhitespace),
            ("",),
        )


class Expression(BNF):
    @classproperty
    def syntax(self):
        return (
            (List,),
            (
                List, OptWhitespace, '|', OptWhitespace, Expression
            ),
        )

    def as_syntax(self):
        value = (self.value[0].as_syntax(),)
        if len(self.value) == 1:
            return value
        else:
            return value + self.value[4].as_syntax()

class SingleLineEnd(BNF):
    @classproperty
    def syntax(self):
        return (
            (OptWhitespace, '\n',),
        )


class LineEnd(BNF):
    @classproperty
    def syntax(self):
        return (
            (SingleLineEnd,),
            (SingleLineEnd, LineEnd),
        )


class List(BNF):
    @classproperty
    def syntax(self):
        return (
            (Term,),
            (Term, OptWhitespace, List,),
        )

    def as_syntax(self):
        val = (self.value[0].as_syntax(),)
        if len(self.value) == 1:
            return val
        else:
            return val + self.value[2].as_syntax()


class Term(BNF):
    @classproperty
    def syntax(self):
        return (
            (Literal,),
            ('<', RuleName, '>'),
        )

    def as_syntax(self):
        if len(self.value) == 1:
            return self.value[0].as_syntax()
        else:
            return self.value[1].as_syntax()


class Literal(BNF):
    @classproperty
    def syntax(self):
        return (
            ('"', Text1, '"',),
            ("'", Text2, "'",),
        )

    def as_syntax(self):
        return self.value[1].as_syntax()


class Text1(BNF):
    @classproperty
    def syntax(self):
        return (
            ("",),
            (Character1, Text1,),
        )

    def as_syntax(self):
        if len(self.value) == 1:
            return self.value[0]
        else:
            return self.value[0].as_syntax() + self.value[1].as_syntax()


class Text2(BNF):
    @classproperty
    def syntax(self):
        return (
            ("",),
            (Character2, Text2,),
        )

    def as_syntax(self):
        if len(self.value) == 1:
            return self.value[0]
        else:
            return self.value[0].as_syntax() + self.value[1].as_syntax()


class Character(BNF):
    @classproperty
    def syntax(self):
        return (
            (Letter,),
            (Digit,),
            (Symbol,),
        )

    def as_syntax(self):
        return self.value[0].as_syntax()


class Letter(BNF):
    syntax = tuple(
        (chr(ord('a') + offset),)
        for offset in range(26)
    ) + tuple(
        (chr(ord('A') + offset),)
        for offset in range(26)
    )

    def as_syntax(self):
        return self.value[0]


class Digit(BNF):
    syntax = tuple(
        (chr(ord('0') + offset),)
        for offset in range(10)
    )

    def as_syntax(self):
        return self.value[0]


class Symbol(BNF):
    syntax = tuple(
        (char,)
        for char in r'| !#$%&()*+,-./:;>=<?@[\]^_`{}~'
    )

    def as_syntax(self):
        return self.value[0]


class Character1(BNF):
    @classproperty
    def syntax(self):
        return (
            (Character,),
            ("'",),
        )

    def as_syntax(self):
        if isinstance(self.value[0], str):
            return self.value[0]
        else:
            return self.value[0].as_syntax()


class Character2(BNF):
    @classproperty
    def syntax(self):
        return (
            (Character,),
            ('"',),
        )

    def as_syntax(self):
        if isinstance(self.value[0], str):
            return self.value[0]
        else:
            return self.value[0].as_syntax()


class RuleName(BNF):
    @classproperty
    def syntax(self):
        return (
            (Letter,),
            (Letter, RuleEnd,),
        )

    def as_syntax(self):
        value = self.value[0].as_syntax()
        if len(self.value) == 1:
            return RuleNameString(value)
        else:
            return RuleNameString(value + self.value[1].as_syntax())


class RuleEnd(BNF):
    @classproperty
    def syntax(self):
        return (
            (OneRuleEnd,),
            (OneRuleEnd, RuleEnd,),
        )

    def as_syntax(self):
        value = self.value[0].as_syntax()
        if len(self.value) == 1:
            return value
        else:
            return value + self.value[1].as_syntax()

class OneRuleEnd(BNF):
    @classproperty
    def syntax(self):
        return (
            (Letter,),
            (Digit,),
            ('-', Letter,),
            ('-', Digit,),
        )

    def as_syntax(self):
        if len(self.value) == 1:
            return self.value[0].as_syntax()
        else:
            return self.value[0] + self.value[1].as_syntax()


class RuleNameString(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Rule({0})'.format(self.value)

    def __repr__(self):
        return str(self)
