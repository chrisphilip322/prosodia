from typing import Tuple, Sequence, Union, TYPE_CHECKING, TypeVar, Callable

from ...core import grammar as g, transform as t
from ...validation.transform_validation import annotate

from ._transform_helpers import identity, identity2

if TYPE_CHECKING:
    T = TypeVar('T')


def _terminal_accum(
    values: Tuple[str, int, Sequence[
        Union[int, Sequence[int]]
    ]]
) -> g.Term:
    _, first, optional_tail = values
    if optional_tail:
        (tail,) = optional_tail
        if isinstance(tail, int):
            return g.LiteralRange(first, tail)
        else:
            return g.Literal(''.join(
                chr(x) for x in [first] + list(tail)
            ))
    else:
        return g.Literal(chr(first))


def _partial_str_to_int(base: int) -> Callable[[Tuple[Sequence[str]]], int]:
    def func(values: Tuple[Sequence[str]]) -> int:
        return int(''.join(values[0]), base=base)

    return func


def _tail_range_accum(values: Tuple[str, int]) -> Union[int, Sequence[int]]:
    return values[1]


def _concat_unit_accum(values: Tuple[str, int]) -> int:
    return values[1]


def add_terminal_transforms(
    lt: t.LanguageTransformation
) -> t.LanguageTransformation:
    lt <<= 'BinaryLiteral', [_terminal_accum]
    lt <<= 'BinaryBody', [_partial_str_to_int(2)]
    lt <<= 'BinaryTail', [
        _tail_range_accum,
        annotate(identity2, T=Sequence[int], T2=Union[int, Sequence[int]])
    ]
    lt <<= 'BinaryConcatUnit', [_concat_unit_accum]
    lt <<= 'HexadecimalLiteral', [_terminal_accum]
    lt <<= 'HexadecimalBody', [_partial_str_to_int(16)]
    lt <<= 'HexadecimalTail', [
        _tail_range_accum,
        annotate(identity2, T=Sequence[int], T2=Union[int, Sequence[int]])
    ]
    lt <<= 'HexadecimalBodyUnit', [
        annotate(identity, T=str),
        annotate(identity, T=str)
    ]
    lt <<= 'HexadecimalConcatUnit', [_concat_unit_accum]
    lt <<= 'DecimalLiteral', [_terminal_accum]
    lt <<= 'DecimalBody', [_partial_str_to_int(10)]
    lt <<= 'DecimalTail', [
        _tail_range_accum,
        annotate(identity2, T=Sequence[int], T2=Union[int, Sequence[int]])
    ]
    lt <<= 'DecimalConcatUnit', [_concat_unit_accum]
    return lt
