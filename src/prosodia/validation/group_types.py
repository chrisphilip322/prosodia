from enum import Enum
from typing import TypeVar, Union, Tuple


T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
T8 = TypeVar('T8')
T9 = TypeVar('T9')
T10 = TypeVar('T10')
T11 = TypeVar('T11')
T12 = TypeVar('T12')
T13 = TypeVar('T13')
T14 = TypeVar('T14')
T15 = TypeVar('T15')


class NoValue(Enum):
    Sentinel = 0


UNV = Union[NoValue, T0]

Group = Tuple[UNV[T0]]
Group2 = Tuple[UNV[T0], UNV[T1]]
Group3 = Tuple[UNV[T0], UNV[T1], UNV[T2]]
Group4 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3]]
Group5 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4]]
Group6 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5]]
Group7 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6]]
Group8 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
               UNV[T7]]
Group9 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
               UNV[T7], UNV[T8]]
Group10 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9]]
Group11 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10]]
Group12 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10], UNV[T11]]
Group13 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10], UNV[T11], UNV[T12]]
Group14 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10], UNV[T11], UNV[T12],
                UNV[T13]]
Group15 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10], UNV[T11], UNV[T12],
                UNV[T13], UNV[T14]]
Group16 = Tuple[UNV[T0], UNV[T1], UNV[T2], UNV[T3], UNV[T4], UNV[T5], UNV[T6],
                UNV[T7], UNV[T8], UNV[T9], UNV[T10], UNV[T11], UNV[T12],
                UNV[T13], UNV[T14], UNV[T15]]
