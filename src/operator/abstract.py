import warnings
from functools import cached_property, wraps
from typing import *

import numpy as np
import pandas as pd
from scipy.stats import norm

from ..field import D0, D1, D2, Field

DfSrs = Union[pd.DataFrame, pd.Series]
DfSrsVar = TypeVar("DfSrsVar", pd.DataFrame, pd.Series)

__all__ = ["AbstractTsOperator"]

N_SNAPSHOTS = 4803


class AbstractTsOperator:
    def __init__(self, fieldtype: Type[Field]):
        self.fieldtype = fieldtype
        self.__op_join__()

    def __op_join__(self):
        self.__op_count__: Dict[str, int] = {}
        self.__op_cache__: Dict[Tuple[str, int], Field] = {}
        for op in self._get_op_list():
            self.__op_count__[op] = 0

    def __op_reset__(self):
        for op in self.__op_count__:
            self.__op_count__[op] = 0

    @classmethod
    def _get_op_list(cls) -> List[str]:
        op_list: List[str] = []
        for i in dir(cls):
            if not i.startswith("_") and i not in ["accumulate", cls.__name__]:
                op_list.append(i)
        return op_list

    def accumulate(
        self,
        x: Field[D1],
        n: int,
        name: str,
        default: Union[Field[D1], None] = None,
        method: str = "back",
    ) -> Union[pd.DataFrame, int]:
        """
        Returns an accumulated 2-dim field.

        Parameters
        ----------
        x : Field[D1]
            1-dim field.
        n : int
            Length of timestamps of the accumulated field.
        name : str
            Operator name.
        default : Union[Field[D1], None], optional
            Default value of the accumulated field, by default None.
        method : str, optional
            Way to accumulate, by default "back".

        Returns
        -------
        Union[pd.DataFrame, int]
            Accumulated field.

        Raises
        ------
        ValueError
            Raised when invalid arguments specified.

        """
        if not name:
            raise ValueError("the operator name cannot be specified as ''")
        count = self.__get_count(name)

        if method == "back":
            self.__accumulate_init(x, n, name, count, default=default)
            return self.__accumulate_back(x, name, count)
        if method == "forward":
            self.__accumulate_init(x, n, name, count, default=default)
            return self.__accumulate_forward(x, name, count)
        if method == "increasing":
            return self.__accumulate_increase(name, count)
        raise ValueError(f"invalid accumulate method: {method}")

    def __accumulate_init(
        self,
        x: Field[D1],
        n: int,
        name: str,
        count: int,
        default: Union[Field[D1], None] = None,
    ) -> None:
        if (name + "_row", count) in self.__op_cache__:
            return
        if default is None:
            default = np.nan
        fld = self.fieldtype(default, timestamps=list(range(n)), tickers=x.tickers)
        self.__op_cache__[(name, count)] = fld
        self.__op_cache__[(name + "_row", count)] = 0

    def __accumulate_back(self, x: Field[D1], name: str, count: int) -> Field[D2]:
        f: Field[D2] = self.__op_cache__[(name, count)]
        f = f.shift(-1)
        f.setrow(f.shape[0] - 1, x)
        self.__op_cache__[(name, count)] = f
        return f

    def __accumulate_forward(self, x: Field[D1], name: str, count: int) -> Field[D2]:
        f: Field[D2] = self.__op_cache__[(name, count)]
        nrow: int = self.__op_cache__[(name + "_row", count)]
        f.setrow(nrow, x)
        self.__op_cache__[(name + "_row", count)] = nrow + 1
        self.__op_cache__[(name, count)] = f
        return f

    def __accumulate_increase(self, name: str, count: int) -> int:
        nrow: int = self.__op_cache__[(name + "_row", count)]
        self.__op_cache__[(name + "_row", count)] = nrow + 1
        return nrow

    def __get_count(self, name: str) -> int:
        if name not in self.__op_count__:
            self.__op_count__[name] = 0
        self.__op_count__[name] += 1
        return self.__op_count__[name]

    def _save(self, x: Any, f_name: str):
        if f_name + "_save" not in self.__op_count__:
            self.__op_count__[f_name + "_save"] = 0
        self.__op_count__[f_name + "_save"] += 1
        _count = self.__op_count__[f_name + "_save"]

        self.__op_cache__[(f_name + "_save", _count)] = x

    def _load(self, f_name: str, default: Any = None) -> Any:
        if f_name + "_load" not in self.__op_count__:
            self.__op_count__[f_name + "_load"] = 0
        self.__op_count__[f_name + "_load"] += 1
        _count = self.__op_count__[f_name + "_load"]

        if (f_name + "_save", _count) not in self.__op_cache__:
            self._save(default, f_name)
        return self.__op_cache__[(f_name + "_save", _count)]
