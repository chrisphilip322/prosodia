# pylint: disable=line-too-long,too-many-return-statements,too-many-branches,too-many-locals
import abc
from typing import Generic, TypeVar

from . import group_types as gt

OutputType = TypeVar('OutputType')


class Switch(Generic[gt.T0, OutputType], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    def __call__(self, group: gt.Group[gt.T0]) -> OutputType:
        (a,) = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        else:
            raise ValueError


class Switch2(
    Generic[gt.T0, gt.T1, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    def __call__(self, group: gt.Group2) -> OutputType:
        a, b = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        else:
            raise ValueError


class Switch3(
    Generic[gt.T0, gt.T1, gt.T2, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    def __call__(self, group: gt.Group3) -> OutputType:
        a, b, c = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        else:
            raise ValueError


class Switch4(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    def __call__(self, group: gt.Group4) -> OutputType:
        a, b, c, d = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        else:
            raise ValueError


class Switch5(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    def __call__(self, group: gt.Group5) -> OutputType:
        a, b, c, d, e = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        else:
            raise ValueError


class Switch6(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    def __call__(self, group: gt.Group6) -> OutputType:
        a, b, c, d, e, f = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        else:
            raise ValueError


class Switch7(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    def __call__(self, group: gt.Group7) -> OutputType:
        a, b, c, d, e, f, g = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        else:
            raise ValueError


class Switch8(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    def __call__(self, group: gt.Group8) -> OutputType:
        a, b, c, d, e, f, g, h = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        else:
            raise ValueError


class Switch9(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    def __call__(self, group: gt.Group9) -> OutputType:
        a, b, c, d, e, f, g, h, i = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        else:
            raise ValueError


class Switch10(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    def __call__(self, group: gt.Group10) -> OutputType:
        a, b, c, d, e, f, g, h, i, j = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        else:
            raise ValueError


class Switch11(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    def __call__(self, group: gt.Group11) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        else:
            raise ValueError


class Switch12(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, gt.T11, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    @abc.abstractmethod
    def case11(self, val: gt.T11) -> OutputType:
        pass

    def __call__(self, group: gt.Group12) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k, l = group  # noqa: E741
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        elif not isinstance(l, gt.NoValue):
            return self.case11(l)
        else:
            raise ValueError


class Switch13(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, gt.T11, gt.T12, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    @abc.abstractmethod
    def case11(self, val: gt.T11) -> OutputType:
        pass

    @abc.abstractmethod
    def case12(self, val: gt.T12) -> OutputType:
        pass

    def __call__(self, group: gt.Group13) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k, l, m = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        elif not isinstance(l, gt.NoValue):
            return self.case11(l)
        elif not isinstance(m, gt.NoValue):
            return self.case12(m)
        else:
            raise ValueError


class Switch14(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, gt.T11, gt.T12, gt.T13, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    @abc.abstractmethod
    def case11(self, val: gt.T11) -> OutputType:
        pass

    @abc.abstractmethod
    def case12(self, val: gt.T12) -> OutputType:
        pass

    @abc.abstractmethod
    def case13(self, val: gt.T13) -> OutputType:
        pass

    def __call__(self, group: gt.Group14) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        elif not isinstance(l, gt.NoValue):
            return self.case11(l)
        elif not isinstance(m, gt.NoValue):
            return self.case12(m)
        elif not isinstance(n, gt.NoValue):
            return self.case13(n)
        else:
            raise ValueError


class Switch15(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, gt.T11, gt.T12, gt.T13, gt.T14, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    @abc.abstractmethod
    def case11(self, val: gt.T11) -> OutputType:
        pass

    @abc.abstractmethod
    def case12(self, val: gt.T12) -> OutputType:
        pass

    @abc.abstractmethod
    def case13(self, val: gt.T13) -> OutputType:
        pass

    @abc.abstractmethod
    def case14(self, val: gt.T14) -> OutputType:
        pass

    def __call__(self, group: gt.Group15) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        elif not isinstance(l, gt.NoValue):
            return self.case11(l)
        elif not isinstance(m, gt.NoValue):
            return self.case12(m)
        elif not isinstance(n, gt.NoValue):
            return self.case13(n)
        elif not isinstance(o, gt.NoValue):
            return self.case14(o)
        else:
            raise ValueError


class Switch16(
    Generic[gt.T0, gt.T1, gt.T2, gt.T3, gt.T4, gt.T5, gt.T6, gt.T7, gt.T8, gt.T9, gt.T10, gt.T11, gt.T12, gt.T13, gt.T14, gt.T15, OutputType],
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def case0(self, val: gt.T0) -> OutputType:
        pass

    @abc.abstractmethod
    def case1(self, val: gt.T1) -> OutputType:
        pass

    @abc.abstractmethod
    def case2(self, val: gt.T2) -> OutputType:
        pass

    @abc.abstractmethod
    def case3(self, val: gt.T3) -> OutputType:
        pass

    @abc.abstractmethod
    def case4(self, val: gt.T4) -> OutputType:
        pass

    @abc.abstractmethod
    def case5(self, val: gt.T5) -> OutputType:
        pass

    @abc.abstractmethod
    def case6(self, val: gt.T6) -> OutputType:
        pass

    @abc.abstractmethod
    def case7(self, val: gt.T7) -> OutputType:
        pass

    @abc.abstractmethod
    def case8(self, val: gt.T8) -> OutputType:
        pass

    @abc.abstractmethod
    def case9(self, val: gt.T9) -> OutputType:
        pass

    @abc.abstractmethod
    def case10(self, val: gt.T10) -> OutputType:
        pass

    @abc.abstractmethod
    def case11(self, val: gt.T11) -> OutputType:
        pass

    @abc.abstractmethod
    def case12(self, val: gt.T12) -> OutputType:
        pass

    @abc.abstractmethod
    def case13(self, val: gt.T13) -> OutputType:
        pass

    @abc.abstractmethod
    def case14(self, val: gt.T14) -> OutputType:
        pass

    @abc.abstractmethod
    def case15(self, val: gt.T15) -> OutputType:
        pass

    def __call__(self, group: gt.Group16) -> OutputType:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = group
        if not isinstance(a, gt.NoValue):
            return self.case0(a)
        elif not isinstance(b, gt.NoValue):
            return self.case1(b)
        elif not isinstance(c, gt.NoValue):
            return self.case2(c)
        elif not isinstance(d, gt.NoValue):
            return self.case3(d)
        elif not isinstance(e, gt.NoValue):
            return self.case4(e)
        elif not isinstance(f, gt.NoValue):
            return self.case5(f)
        elif not isinstance(g, gt.NoValue):
            return self.case6(g)
        elif not isinstance(h, gt.NoValue):
            return self.case7(h)
        elif not isinstance(i, gt.NoValue):
            return self.case8(i)
        elif not isinstance(j, gt.NoValue):
            return self.case9(j)
        elif not isinstance(k, gt.NoValue):
            return self.case10(k)
        elif not isinstance(l, gt.NoValue):
            return self.case11(l)
        elif not isinstance(m, gt.NoValue):
            return self.case12(m)
        elif not isinstance(n, gt.NoValue):
            return self.case13(n)
        elif not isinstance(o, gt.NoValue):
            return self.case14(o)
        elif not isinstance(p, gt.NoValue):
            return self.case15(p)
        else:
            raise ValueError
