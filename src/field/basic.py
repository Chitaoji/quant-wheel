"""
Contains a pandas implemention of Field.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import Any, Optional, Union

from ._types import D1, Field, Num
from .abstract import AbstractField

__all__ = ["PandasField"]


class PandasField(AbstractField):
    """A pandas implemention of Field."""

    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        ...

    def expand(self, tickers: list, timestamps: Optional[list] = None) -> "Field":
        """Abstract method."""

    def shift(self, n: int = 1) -> None:
        """Abstract method."""

    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Abstract method."""
