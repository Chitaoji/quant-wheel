"""
Contains typing classes: Field, Num, D0, D1, D2, Dim, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import abstractmethod
from typing import Any, Generic, Optional, Tuple, Type, TypeVar, Union, overload

from .._types import _NeverInstantiate, _NeverInstantiateMeta

Data = Union["D0", "D1", "D2"]
D = TypeVar("D", "D0", "D1", "D2")

__all__ = ["Field", "Num", "D0", "D1", "D2", "Data"]


class _D0Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return isinstance(__instance, (int, float))


class _D1Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 1


class _D2Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 2


class D0(metaclass=_D0Meta):
    """
    D0 stands for 0-dimensional data, usually refering to ints and floats.

    """


Num = D0  # `Num` is a human-readable alias for `D0`


class D1(metaclass=_D1Meta):
    """D1 stands for 1-dimensional data."""

    shape: Tuple[int]


class D2(metaclass=_D2Meta):
    """D2 stands for 2-dimensional data."""

    shape: Tuple[int, int]

    @abstractmethod
    def __init__(self) -> None:
        ...


class _TickersDescriptor(_NeverInstantiate):
    @overload
    def __get__(self, instance: "Field[D0]", owner: Any) -> None:
        ...

    @overload
    def __get__(self, instance: "Field[D1]", owner: Any) -> list:
        ...

    @overload
    def __get__(self, instance: "Field[D2]", owner: Any) -> list:
        ...


class _TimestampsDescriptor(_NeverInstantiate):
    @overload
    def __get__(self, instance: "Field[D0]", owner: Any) -> None:
        ...

    @overload
    def __get__(self, instance: "Field[D1]", owner: Any) -> None:
        ...

    @overload
    def __get__(self, instance: "Field[D2]", owner: Any) -> list:
        ...


class _ShapeDescriptor(_NeverInstantiate):
    @overload
    def __get__(self, instance: "Field[D0]", owner: Any) -> Tuple[()]:
        ...

    @overload
    def __get__(self, instance: "Field[D1]", owner: Any) -> Tuple[int]:
        ...

    @overload
    def __get__(self, instance: "Field[D2]", owner: Any) -> Tuple[int, int]:
        ...


class _FieldMeta(_NeverInstantiateMeta):
    use_instead = "field()"


class Field(Generic[D], metaclass=_FieldMeta):
    """Field structure."""

    data: D
    dim: Type[D]
    tickers: _TickersDescriptor
    timestamps: _TimestampsDescriptor
    shape: _ShapeDescriptor

    @overload
    def __init__(self: "Field[D0]", data: Any) -> None:
        ...

    @overload
    def __init__(
        self: "Field[D1]",
        data: Any,
        tickers: Optional[list] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self: "Field[D2]",
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        ...

    def shift(self: "Field[D2]", n: int = 1) -> None:
        """
        Shift timestamps by desired number of periods with an optional time n.

        Parameters
        ----------
        n : int
            Number of periods to shift.

        """

    def setrow(self: "Field[D2]", n: int, value: Union[Num, "Field[D1]"]) -> None:
        """
        Set a row in a 2-dimensional field with a given value.

        Parameters
        ----------
        n : int
            Represents the index of the row that you want to set in the field.
        value : Union[Num, Field[D1]]
            Value to be set, can be either a number (`Num`) or a 1-dimensional
            field (`Field[D1]`).

        """
