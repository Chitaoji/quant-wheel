"""
Contains the abstract classes: Field, D1, D2, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Optional, Tuple, TypeVar, Union, overload

from attrs import define
from attrs import field as attrs_field  # Avoid confusion with the field we export.

D = TypeVar("D", "D1", "D2")

__all__ = ["Field", "D1", "D2"]


class D1Type(ABCMeta):
    """Metaclass of D1."""

    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 1


class D2Type(ABCMeta):
    """Metaclass of D2."""

    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 2


class D1(metaclass=D1Type):
    """
    D1 stands for 1-dimension.

    """

    @abstractmethod
    def __init__(self):
        ...

    @property
    @abstractmethod
    def shape(self) -> Tuple[int]:
        """
        Shape of data.

        Returns
        -------
        Tuple[int]
            1-dimensional Tuple.

        """


class D2(metaclass=D2Type):
    """
    D2 stands for 2-dimension.

    """

    @abstractmethod
    def __init__(self):
        ...

    @property
    @abstractmethod
    def shape(self) -> Tuple[int, int]:
        """
        Shape of data.

        Returns
        -------
        Tuple[int, int]
            2-dimensional Tuple.

        """


@define
class Field(Generic[D]):
    """Abstract field type."""

    data: D
    tickers: Optional[list] = attrs_field(default=None)
    timestamps: Optional[list] = attrs_field(default=None)
    __dim: Union[D1Type, D2Type] = attrs_field(init=False, alias="__dim")

    def __attrs_post_init__(self) -> None:
        if isinstance(self.data, D1):
            self.__dim = D1
        elif isinstance(self.data, D2):
            self.__dim = D2
        else:
            raise TypeError(
                f"attribute 'data' should be of type 'D1' or 'D2', got '{type(self.data).__name__}'"
            )

    @overload
    @property
    def dim(self: "Field[D1]") -> D1Type:
        ...

    @overload
    @property
    def dim(self: "Field[D2]") -> D2Type:
        ...

    @property
    def dim(self):
        """Dimension of the data."""
        return self.__dim
