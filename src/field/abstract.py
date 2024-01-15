"""
Contains the abstract class: AbstractField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import Any, Optional, Tuple, Type, Union, final

from ..abcv import ABCV, MethodCallError, MethodImplementionError, abstractmethodval
from ._types import D0, D1, D2, Data, Field, Num, get_shape

__all__ = ["AbstractField"]


class AbstractField(ABCV):
    """Abstract field type."""

    data: Data
    dim: Type[Data]
    tickers: Optional[list]
    timestamps: Optional[list]
    shape: Tuple[int, ...]

    # ===================================================
    # User must implement these:
    @abstractmethodval
    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        """
        Initialzing and setting three attributes of the instance: self.data,
        self.tickers, and self.timestamps. See `Field.__init__()`.

        """

    @abstractmethodval
    def shift(self, n: int = 1) -> Field[D2]:
        """Method for D2 only. See `Field.shift()`."""

    @abstractmethodval
    def setrow(self, n: int, value: Union[Num, Field[D1]]) -> None:
        """Method for D2 only. See `Field.setrow()`."""

    # ===================================================

    def __repr__(self) -> str:
        return repr(self.data)

    @final
    @__init__.after
    def __field_post_init__(self, result: None) -> None:
        self.__check_return_is_none(result)
        if isinstance(self.data, D0):
            self.dim = D0  # Automatically set the attribute 'dim'.
            self.__check_attr_is_none("tickers")
            self.__check_attr_is_none("timestamps")
        elif isinstance(self.data, D1):
            self.dim = D1
            self.__check_attr_is_none("timestamps")
        elif isinstance(self.data, D2):
            self.dim = D2
        else:
            raise MethodImplementionError(
                f"attribute 'data' must be of type D0, D1, or D2, got {type(self.data)}."
            )
        self.shape = get_shape(self.data)  # Automatically set the attribute 'shape'.

    @final
    @shift.before
    @setrow.before
    def _on_field_d2(self, *_, **__) -> None:
        if self.dim is not D2:
            raise MethodCallError(
                f"calling this method requires dim = D2, got dim = {self.dim}."
            )

    @final
    @shift.after
    def _return_d2(self, result: Field[D2]) -> None:
        self.__check_return_is_d2(result)

    @final
    @setrow.after
    def _return_none(self, result: None) -> None:
        self.__check_return_is_none(result)

    def __check_attr_is_none(self, __name: str) -> None:
        if (v := getattr(self, __name)) is not None:
            raise MethodImplementionError(
                f"attribute '{__name}' must be None when dim = {self.dim}, got {v}."
            )

    def __check_return_is_none(self, __return: Any) -> None:
        if __return is not None:
            raise MethodImplementionError(
                f"function return must be None, got {__return}."
            )

    def __check_return_is_d2(self, __return: Any) -> None:
        if isinstance(__return, AbstractField) and __return.dim is D2:
            return
        raise MethodImplementionError(
            f"function result must be of type Field[D2], got {type(__return)}."
        )
