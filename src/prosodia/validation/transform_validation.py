from functools import wraps
from inspect import signature
from typing import Iterable, Callable, get_type_hints, Union, Tuple

from .validity import Validity


def annotate(func: Callable, **hints: Union[type, None]) -> Callable:
    try:
        get_type_hints(func, {}, {})
    except NameError:
        pass
    else:
        raise ValueError(
            'expecting to be able to substitute some forward references'
        )

    @wraps(func)
    def annotated(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)
    annotated.__annotations__ = get_type_hints(func, hints, {})
    return annotated


def get_return_type(func: Callable) -> type:
    sig = signature(func, follow_wrapped=False)
    anno = sig.return_annotation
    if anno is sig.empty:
        raise TypeError('func doesn\'t have a return type annotation')
    return anno


def check_composability(
    argument_types: Iterable[type],
    target_func: Callable
) -> Validity:
    argument_types = [Tuple[tuple(argument_types)]]
    parameter_hints = get_type_hints(target_func)
    parameter_types = [
        parameter_hints[param_name]
        for param_name in signature(target_func).parameters.keys()
    ]
    if argument_types == parameter_types:
        return Validity.valid()
    else:
        return Validity.invalid(
            'arguments are not composable with parameters: ({0}), ({1})'.format(
                argument_types, parameter_types
            )
        )


def check_isomorphic(
    funcs: Iterable[Callable]
) -> bool:
    first, *rest = (get_return_type(func) for func in funcs)
    return all(
        first == rtype
        for rtype in rest
    )
