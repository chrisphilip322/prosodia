import typing

if typing.TYPE_CHECKING:
    T = typing.TypeVar('T')
    T2 = typing.TypeVar('T2')
    T3 = typing.TypeVar('T3')
    Addable = typing.TypeVar('Addable', str, typing.List[object])


def list_of(
    values: typing.Tuple['T']
) -> typing.List['T']:
    return [values[0]]


def push_list(
    values: typing.Tuple['T', typing.List['T']]
) -> typing.List['T']:
    return [values[0]] + values[1]


def nothing(_: typing.Tuple['T']) -> None:
    return None


def nothing2(_: typing.Tuple['T', 'T2']) -> None:
    return None


def nothing3(_: typing.Tuple['T', 'T2', 'T3']) -> None:
    return None


def identity(values: typing.Tuple['T']) -> 'T':
    return values[0]


def identity2(values: typing.Tuple['T']) -> 'T2':
    return values[0]  # type: ignore


def unescape(
    values: typing.Tuple[str, 'T', str]
) -> 'T':
    return values[1]


def add(
    values: typing.Tuple['Addable', 'Addable']
) -> 'Addable':
    iterable = iter(values)
    accum = next(iterable)
    for item in iterable:
        accum += item
    return accum
