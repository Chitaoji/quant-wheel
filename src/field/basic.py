"""
Contains a pandas implemention of Field: PandasField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import TYPE_CHECKING, Any, Optional, Union

import pandas as pd

from ._types import D0, D1, D2, Field, Num, get_shape
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
        name: Optional[str] = None,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        if isinstance(data, Num):
            if tickers and timestamps:
                self.data = pd.DataFrame(data, columns=tickers, index=timestamps)
                self.dim = D2
            elif tickers:
                self.data, self.dim = pd.Series(data, index=tickers), D1
            else:
                self.data, self.dim = data, D0
            self.tickers, self.timestamps = tickers, timestamps
        elif isinstance(data, pd.Series):
            self.data, self.dim, self.timestamps = data, D1, None
            if tickers:
                self.data.index = tickers
            self.tickers = self.data.index.tolist()
        elif isinstance(data, pd.DataFrame):
            self.data, self.dim = data, D2
            if tickers:
                self.data.columns = tickers
            if timestamps:
                self.data.index = timestamps
            self.tickers = self.data.columns.tolist()
            self.timestamps = self.data.index.tolist()
        else:
            raise TypeError(
                "argument 'data' must be of type Num, Series, or DataFrame, "
                f"got {type(data)}"
            )
        self.name = name if name else "temp"
        self.shape = get_shape(self.data)

    def shift(self, n: int = 1) -> None:
        """Implementing `AbstractField.shift()`."""
        return self.__class__(
            self.data.shift(n), tickers=self.tickers, timestamps=self.timestamps
        )

    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Implementing `AbstractField.setrow()`."""
        self.data.iloc[n] = value

    def __repr__(self) -> str:
        return super().__repr__() + "\n" + repr(self.data)
