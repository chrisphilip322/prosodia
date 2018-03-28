#!/usr/bin/env python

import typing

T = typing.TypeVar('T')

def identity(x: T) -> T:
    return x

def fizz(x: T, func: typing.Callable[[T], str]) -> str:
    return func(x)

a = fizz(5, str)
b = fizz('a', identity)
c = fizz(identity(6), str)
