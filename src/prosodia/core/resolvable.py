import abc
from collections import deque
import functools
import typing

InputType = typing.TypeVar('InputType')
OutputType = typing.TypeVar('OutputType')


class Resolvable(typing.Generic[OutputType], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def resolve(self, d: deque) -> typing.Union['Resolvable[OutputType]', OutputType]:
        pass


class ResolvableFunc(functools.partial, Resolvable[OutputType]):
    def resolve(self, _: deque) -> typing.Union[Resolvable[OutputType], OutputType]:
        return self()


class ResolvablePair(Resolvable[OutputType], typing.Generic[InputType, OutputType]):
    def __init__(
        self,
        resolvable: Resolvable[InputType],
        next_resolvable: typing.Callable[[InputType], Resolvable[OutputType]]
    ) -> None:
        self.resolvable = resolvable
        self.next_resolvable = next_resolvable

    def resolve(self, d: deque) -> typing.Union[Resolvable[OutputType], OutputType]:
        d.append(self.next_resolvable)
        return self.resolvable  # type: ignore


def _identity(x: OutputType) -> OutputType:
    return x


def resolve(result: typing.Any) -> OutputType:
    d = deque([_identity])
    while d:
        result = d.pop()(result)
        while isinstance(result, Resolvable):
            result = result.resolve(d)  # typing: ignore
    return result


def resolve_map(
    values: typing.Sequence[InputType],
    func: typing.Callable[[InputType], OutputType]
) -> Resolvable[typing.List[OutputType]]:
    return _resolve_map_impl(list(values), func, 0, [])


def _resolve_map_impl(
    values: typing.Sequence[InputType],
    func: typing.Callable[[InputType], OutputType],
    index: int,
    result: typing.List[OutputType]
) -> Resolvable[typing.List[OutputType]]:
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
    values: typing.Sequence[InputType],
    func: typing.Callable[[InputType], OutputType],
    index: int,
    result: typing.List[OutputType],
    value: OutputType,
) -> Resolvable[typing.List[OutputType]]:
    return ResolvableFunc(
        _resolve_map_impl,
        values,
        func,
        index + 1,
        result + [value]
    )
