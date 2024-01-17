"""
Contains a pandas implemention of Field: PandasField.

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

    data: Union["DataFrame", "Series", Num]

    def __init__(
        self,
        data: Any,
        /,
        name: Optional[str] = None,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> Tuple[Data, list, list]:
        if isinstance(data, Num):
            if tickers and timestamps:
                self.data = pd.DataFrame(data, columns=tickers, index=timestamps)
            elif tickers:
                self.data = pd.Series(data, index=tickers)
            else:
                self.data = data
            self.tickers, self.timestamps = tickers, timestamps
        elif isinstance(data, pd.Series):
            tickers = tickers if tickers else data.index.tolist()
            self.data, self.tickers, self.timestamps = data, tickers, None
        elif isinstance(data, pd.DataFrame):
            tickers = tickers if tickers else data.index.tolist()
            timestamps = timestamps if timestamps else data.index.tolist()
            self.data, self.tickers, self.timestamps = data, tickers, timestamps
        else:
            raise TypeError(
                "argument 'data' must be of type Num, Series, or DataFrame, "
                f"got {type(data)}"
            )

    def shift(self, n: int = 1) -> None:
        """Implementing `AbstractField.shift()`."""
        return PandasField(
            self.data.shift(n), tickers=self.tickers, timestamps=self.timestamps
        )

    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Implementing `AbstractField.setrow()`."""
        self.data.iloc[n] = value
