"""
Contains a pandas implemention of Field.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

import pandas as pd

from ._types import D1, Data, Field, Num
from .abstract import AbstractField

if TYPE_CHECKING:
    from pandas import DataFrame, Series

__all__ = ["PandasField"]


class PandasField(AbstractField):
    """A pandas implemention of Field."""

    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> Tuple[Data, list, list]:
        if isinstance(data, Num):
            self.data, self.tickers, self.timestamps = data, None, None
        elif isinstance(data, pd.Series):
            tickers = tickers if tickers else data.index.tolist()
            self.data, self.tickers, self.timestamps = data, tickers, None
        elif isinstance(data, pd.DataFrame):
            tickers = tickers if tickers else data.index.tolist()
            timestamps = timestamps if timestamps else data.index.tolist()
            self.data, self.tickers, self.timestamps = data, tickers, timestamps
        else:
            self.data, self.tickers, self.timestamps = data, None, None

    def shift(self, n: int = 1) -> None:
        """Abstract method."""

    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Abstract method."""
