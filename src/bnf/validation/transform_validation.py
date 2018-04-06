import typing

if typing.TYPE_CHECKING:
    from ..core.grammar import Language, Rule  # pylint: disable=unused-import
    from ..core.transform import LanguageTransformation, RuleTransformation  # pylint: disable=unused-import

S = typing.TypeVar('S')
T = typing.TypeVar('T')
Type_ = typing.Union[type, typing.GenericMeta]


class Validity(object):
    def __init__(self, messages: typing.Sequence[str]) -> None:
        self.messages = messages

    @classmethod
    def valid(cls) -> 'Validity':
        return cls(list())

    @classmethod
    def invalid(cls, msg: str, *msgs: str):
        return cls([msg]+list(msgs))

    def __bool__(self) -> bool:
        return not bool(self.messages)

    def __add__(self, other: typing.Any) -> 'Validity':
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return Validity(
                list(self.messages) + list(other.messages)
            )

class TypeAdder(typing.Generic[S, T]):
    def __init__(self, func: typing.Callable[[S], T]) -> None:
        self.func = func

    def __getitem__(
        self,
        types: typing.Tuple[typing.Sequence[Type_], Type_]
    ) -> 'TypedFunc[S, T]':
        input_type, output_type = types
        return TypedFunc(
            self.func,
            typing.Tuple[tuple(input_type)],
            output_type
        )


def _get_input_type(func: typing.Callable[[typing.Any], typing.Any]) -> Type_:
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
        input_type: Type_,
        output_type: Type_
    ) -> None:
        self.func = func
        self.input_type = input_type
        self.output_type = output_type

    def __call__(self, values: S) -> T:
        return self.func(values)

    @classmethod
    def get_input(cls, func: typing.Callable) -> Type_:
        return (
            func.input_type
            if isinstance(func, cls)
            else _get_input_type(func)
        )

    @classmethod
    def get_output(cls, func: typing.Callable) -> Type_:
        return (
            func.output_type
            if isinstance(func, cls)
            else func.__annotations__['return']
        )

    @classmethod
    def assert_composable(
        cls,
        outputs: typing.Iterable[typing.Callable],
        input_: typing.Callable
    ) -> bool:
        output_types = (
            TypedFunc.get_output(i)
            for i in outputs
        )
        input_type = TypedFunc.get_input(input_)
        output_type = typing.Tuple[tuple(output_types)]
        return input_type == output_type

    @classmethod
    def assert_substitutable(
        cls,
        funcs: typing.Iterable[typing.Callable]
    ) -> bool:
        ifuncs = iter(funcs)
        first = TypedFunc.get_output(next(ifuncs))
        return all(first == TypedFunc.get_output(other) for other in ifuncs)
