import abc
from collections import deque
import functools
import typing

I = typing.TypeVar('I')
O = typing.TypeVar('O')

class Resolvable(typing.Generic[O], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def resolve(self, d: deque) -> typing.Union['Resolvable[O]', O]:
        pass

class ResolvableFunc(functools.partial, Resolvable[O]):
    def resolve(self, _: deque) -> typing.Union[Resolvable[O], O]:
        return self()

class ResolvablePair(Resolvable[O], typing.Generic[I, O]):
    def __init__(
        self,
        resolvable: Resolvable[I],
        next_resolvable: typing.Callable[[I], Resolvable[O]]
    ) -> None:
        self.resolvable = resolvable
        self.next_resolvable = next_resolvable

    def resolve(self, d: deque) -> typing.Union[Resolvable[O], O]:
        d.append(self.next_resolvable)
        return self.resolvable # type: ignore

def _identity(x: O) -> O:
    return x

def resolve(result: typing.Any) -> O:
    d = deque([_identity])
    while d:
        result = d.pop()(result)
        while isinstance(result, Resolvable):
            result = result.resolve(d) # typing: ignore
    return result


def resolve_map(
    values: typing.Sequence[I],
    func: typing.Callable[[I], O]
) -> Resolvable[typing.List[O]]:
    return _resolve_map_impl(list(values), func, 0, [])

def _resolve_map_impl(
    values: typing.Sequence[I],
    func: typing.Callable[[I], O],
    index: int,
    result: typing.List[O]
) -> Resolvable[typing.List[O]]:
    if index >= len(values):
        return ResolvableFunc(
            _identity,
            result
        )
    else:
        return ResolvablePair(
            ResolvableFunc(func, values[index]),
            functools.partial(
                _update_result,
                values,
                func,
                index,
                result
            )
        )

def _update_result(
    values: typing.Sequence[I],
    func: typing.Callable[[I], O],
    index: int,
    result: typing.List[O],
    value: O,
) -> Resolvable[typing.List[O]]:
    return ResolvableFunc(
        _resolve_map_impl,
        values,
        func,
        index + 1,
        result + [value]
    )
