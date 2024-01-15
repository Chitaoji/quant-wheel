"""
Contains typing classes: Field, Num, D0, D1, D2, Dim, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import Any, Generic, Optional, Tuple, Type, TypeVar, Union, overload

from .._types import _NeverInstantiate, _NeverInstantiateMeta

Data = Union["D0", "D1", "D2"]
D = TypeVar("D", "D0", "D1", "D2")

__all__ = ["Field", "Num", "D0", "D1", "D2", "Data", "get_shape"]


class _D0Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return isinstance(__instance, (int, float))

    def __repr__(cls) -> str:
        return cls.__name__


class D0(metaclass=_D0Meta):
    """
    D0 stands for 0-dimensional data, usually refering to ints and floats.

    """


Num = D0  # `Num` is a human-readable alias for `D0`.


class _D1Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 1

    def __repr__(cls) -> str:
        return cls.__name__


class D1(metaclass=_D1Meta):
    """D1 stands for 1-dimensional data."""

    shape: Tuple[int]


class _D2Meta(_NeverInstantiateMeta):
    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 2

    def __repr__(cls) -> str:
        return cls.__name__


class D2(metaclass=_D2Meta):
    """D2 stands for 2-dimensional data."""

    shape: Tuple[int, int]


@overload
def get_shape(data: D0) -> Tuple[()]:
    ...


@overload
def get_shape(data: D1) -> Tuple[int]:
    ...


@overload
def get_shape(data: D2) -> Tuple[int, int]:
    ...


def get_shape(data: Data) -> Tuple[int, ...]:
    """
    Get the shape of a Data object.

    Parameters
    ----------
    data : Data
        A Data object.

    Returns
    -------
    Tuple[int, ...]
        Tuple of ints.

    """
    if isinstance(data, D0):
        return tuple()
    return data.shape


class _DimDescriptor(_NeverInstantiate):
    @overload
    def __get__(self, instance: "Field[D0]", owner: Any) -> Type[D0]:
        ...

    @overload
    def __get__(self, instance: "Field[D1]", owner: Any) -> Type[D1]:
        ...

    @overload
    def __get__(self, instance: "Field[D2]", owner: Any) -> Type[D2]:
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
    dim: _DimDescriptor
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

    def shift(self: "Field[D2]", n: int = 1) -> "Field[D2]":
        """
        Shift timestamps by desired number of periods with an optional time n.

        Parameters
        ----------
        n : int
            Number of periods to shift.

        """

    def setrow(self: "Field[D2]", n: int, value: Union[Num, "Field[D1]"]) -> None:
        """
        Set a row in the 2-dimensional field with a given value.

        Parameters
        ----------
        n : int
            Represents the index of the row to be set in the field.
        value : Union[Num, Field[D1]]
            Value to set with, can be either a number (`Num`) or a 1-dimensional
            field (`Field[D1]`).

        """
