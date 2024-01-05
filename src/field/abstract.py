"""
Contains the abstract classes: Field, D1, D2, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Optional, Tuple, Type, TypeVar, Union

from attrs import define
from attrs import field as attrs_field  # Avoid confusion with the field we export.

D = TypeVar("D", "D1", "D2")


__all__ = ["Field", "Num", "D1", "D2"]


class Num(metaclass=ABCMeta):
    """Num includes int and float."""

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        if cls is Num:
            return issubclass(__subclass, (int, float))
        return False


class D1Meta(ABCMeta):
    """Metaclass of D1."""

    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 1


class D2Meta(ABCMeta):
    """Metaclass of D2."""

    def __instancecheck__(cls, __instance: Any) -> bool:
        return hasattr(__instance, "shape") and len(getattr(__instance, "shape")) == 2


class D1(metaclass=D1Meta):
    """
    D1 stands for 1-dimension.

    """

    @abstractmethod
    def __init__(self) -> None:
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


class D2(metaclass=D2Meta):
    """
    D2 stands for 2-dimension.

    """

    @abstractmethod
    def __init__(self) -> None:
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

    def __init__(
        self,
        data: Union[D, Num],
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        self.tickers = tickers
        self.timestamps = timestamps
        if isinstance(data, Num):
            self.create_empty()
            self.fill(data)
        elif isinstance(data, D1):
            self.data: D = data
            self.dim: Type[D] = D1
        elif isinstance(data, D2):
            self.data = data
            self.dim = D2
        else:
            raise TypeError(
                f"attribute 'data' should be of type 'D1' or 'D2', got '{type(data).__name__}'"
            )

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.data.shape

    @abstractmethod
    def create_empty(self) -> None:
        """
        Create an empty memory space for the data.

        """

    @abstractmethod
    def fill(self, value: Num) -> None:
        """
        Fill the data with value.

        Parameters
        ----------
        value : Num
            Value to fill with.

        """

    @abstractmethod
    def shift(self, n: int = 1) -> None:
        """
        Shift timestamps by desired number of periods with an optional time n.

        Parameters
        ----------
        n : int
            Number of periods to shift.

        """

    @abstractmethod
    def insert(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """
        Inserts the value at position `n` in the data structure.

        Parameters
        ----------
        n : int
            Represents the index at which the value should be inserted.
        value : Union[Num, Field[D1]]
            Value to be inserted.

        """
