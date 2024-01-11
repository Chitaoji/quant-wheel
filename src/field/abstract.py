"""
Contains the abstract class: AbstractField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import Any, Callable, Optional, Type, TypeVar, Union, final

from ..abcv import ABCV, MethodImplementionError, abstractmethodval
from ._types import D0, D1, D2, Data, Field, Num

C = TypeVar("C", bound=Callable)

__all__ = ["AbstractField"]


class AbstractField(ABCV):
    """Abstract field type."""

    @abstractmethodval
    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        """Initialzing. See `Field.__init__()`."""

    @abstractmethodval
    def shift(self, n: int = 1) -> None:
        """Method for D2 only. See `Field.shift()`."""

    @abstractmethodval
    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Method for D2 only. See `Field.setrow()`."""

    @final
    @__init__.val
    def _init_validator(self) -> None:
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
            raise MethodImplementionError(
                f"attribute 'data' must be of type D0, D1 or D2, got {type(data)}."
            )
        setattr(self, "dim", dim)

    @final
    @shift.val
    def _shift_validator(self) -> None:
        print("check shift")

    @final
    @setrow.val
    def _setrow_validator(self) -> None:
        print("check setrow")

    def __check_attr_is_none(self, __name: str, __dim: Type[Data]) -> None:
        if (v := getattr(self, __name)) is not None:
            raise MethodImplementionError(
                f"attribute '{__name}' must be None when dim = {__dim.__name__}, got {v}."
            )
