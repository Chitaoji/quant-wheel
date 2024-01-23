"""
Contains a pandas implemention of Field: PandasField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from functools import cached_property
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

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
        elif isinstance(data, pd.Series):
            self.data, self.dim = data, D1
            if tickers:
                self.data.index = tickers
        elif isinstance(data, pd.DataFrame):
            self.data, self.dim = data, D2
            if tickers:
                self.data.columns = tickers
            if timestamps:
                self.data.index = timestamps
        else:
            raise TypeError(
                "argument 'data' must be of type Num, Series, or DataFrame, "
                f"got {type(data)}"
            )
        self.name = name if name else "temp"

    def shift(self, n: int = 1) -> None:
        """Implementing `AbstractField.shift()`."""
        return self.__class__(
            self.data.shift(n), tickers=self.tickers, timestamps=self.timestamps
        )

    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Implementing `AbstractField.setrow()`."""
        if isinstance(value, Num):
            self.data.iloc[n] = value
        elif isinstance(value, PandasField):
            self.data.iloc[n] = value.data
        else:
            raise TypeError(f"argument 'value' has an illegal type: {type(value)}")

    def __repr__(self) -> str:
        if self.dim is D0:
            return super().__repr__() + f"={self.data}"
        return super().__repr__() + "\n" + repr(self.data)

    @cached_property
    def tickers(self) -> list:
        """List of tickers."""
        if self.dim is D1:
            return self.data.index.to_list()
        elif self.dim is D2:
            return self.data.columns.to_list()
        return None

    @cached_property
    def timestamps(self) -> list:
        """List of timestamps."""
        if self.dim is D2:
            return self.data.index.to_list()
        return None

    @cached_property
    def shape(self) -> Tuple[int, ...]:
        """Data shape"""
        return get_shape(self.data)
