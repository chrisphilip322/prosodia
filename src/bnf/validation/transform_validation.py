import typing

S = typing.TypeVar('S')
T = typing.TypeVar('T')
_Type = typing.Union[type, typing.GenericMeta]

class TypeAdder(typing.Generic[S, T]):
    def __init__(self, func: typing.Callable[[S], T]) -> None:
        self.func = func

    def __getitem__(
        self,
        types: typing.Tuple[typing.Sequence[_Type], _Type]
    ) -> 'TypedFunc[S, T]':
        input_type, output_type = types
        return TypedFunc(
            self.func,
            typing.Tuple[tuple(input_type)],
            output_type
        )


def get_input_type(func: typing.Callable[[T], typing.Any]) -> _Type:
    items = iter(func.__annotations__.items())
    a_name, a_type = next(items)
    _, b_type = next(items)
    try:
        next(items)
    except StopIteration:
        if a_name != 'return':
            return a_type
        else:
            return b_type
    else:
        raise ValueError('func should only take one input')


class TypedFunc(typing.Generic[S, T]):
    def __init__(
        self,
        func: typing.Callable[[S], T],
        input_type: _Type,
        output_type: _Type
    ) -> None:
        self.func = func
        self.input_type = input_type
        self.output_type = output_type

    def __call__(self, values: S) -> T:
        return self.func(values)

    @classmethod
    def validate(
        cls,
        inputs: typing.Sequence[typing.Callable],
        output: typing.Callable
    ) -> bool:
        input_types = (
            i.output_type if isinstance(i, cls) else i.__annotations__['return']
            for i in inputs
        )
        output_type = (
            output.input_type
            if isinstance(output, cls)
            else get_input_type(output)
        )
        input_type = typing.Tuple[tuple(input_types)]
        return input_type == output_type
