"""
Contains the abstract class: AbstractField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Type, Union, cast, final

from ._types import D0, D1, D2, Data, Field, Num

__all__ = ["AbstractField"]


class _AbstractFieldMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        if isinstance(cls, AbstractField):
            self = cast(AbstractField, cls.__new__(cls, *args, **kwargs))
            self.__init__(*args, **kwargs)
            self.__field_post_init__()
            return self
        else:
            raise TypeError(
                f"_AbstractFieldMeta can only be used as the metaclass of AbstractField, \
but the class was {type(cls)}"
            )


class AbstractField(metaclass=_AbstractFieldMeta):
    """Abstract field type."""

    @abstractmethod
    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        """Initialzing."""

    @abstractmethod
    def shift(self, n: int = 1) -> None:
        """Method for D2 only."""

    @abstractmethod
    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Method for D2 only."""

    @final
    def __field_post_init__(self) -> None:
        data = getattr(self, "data")
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
                f"attribute 'data' must be of type D0, D1 or D2, got {type(data)}"
            )
        setattr(self, "dim", dim)

    def __check_attr_is_none(self, __name: str, __dim: Type[Data]) -> None:
        if v := getattr(self, __name) is not None:
            raise ValueError(
                f"{__name} must be None when dim = {__dim.__name__}, got {v}"
            )
