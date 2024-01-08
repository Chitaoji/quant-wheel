"""
Contains the abstract class: AbstractField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union

from ._types import D0, D1, D2, Dim, Field, Num

__all__ = ["AbstractField"]


class AbstractField(ABC):
    """Abstract field type."""

    @abstractmethod
    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        ...

    @abstractmethod
    def expand(self, tickers: list, timestamps: Optional[list] = None) -> "Field":
        """Abstract method for D1 only."""

    @abstractmethod
    def shift(self, n: int = 1) -> None:
        """Abstract method for D2 only."""

    @abstractmethod
    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Abstract method for D2 only."""

    # Tools maybe helpful
    def _check_data_dim(self, data: Any) -> Type[Dim]:
        if isinstance(data, D0):
            dim = D0
            self.__check_attr_is_none("tickers", dim)
            self.__check_attr_is_none("timestamps", dim)
        elif isinstance(data, D1):
            dim = D1
            self.__check_attr_is_none("timestamps", dim)
        elif isinstance(data, D2):
            dim = D2
        else:
            raise TypeError(
                f"attribute 'data' should be of type D0, D1 or D2, got {type(data).__name__}"
            )
        return dim

    def __check_attr_is_none(self, __name: str, __dim: Type[Dim]) -> None:
        if v := getattr(self, __name) is not None:
            raise ValueError(
                f"{__name} should be None when dim = {__dim.__name__}, got {v}"
            )
