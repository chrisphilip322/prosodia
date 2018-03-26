#!/usr/bin/env python

from functools import singledispatch
import typing

@singledispatch
def func(x: typing.Any) -> typing.Any:
    print(x)
    return x

@func.register(int)
def func_int(x: int) -> typing.Tuple[int]:
    print('int', x*2)
    return (x,)

@func.register(tuple)
def func_tuple(x: typing.Tuple[str]) -> str:
    print('tuple', x)
    return 'unpacked {0}'.format(x[0])

a = func(5)
b = func(a)
