import warnings
from functools import cached_property, wraps
from typing import *

import numpy as np
import pandas as pd
from scipy.stats import norm

from ..field import D1, Field

DfSrs = Union[pd.DataFrame, pd.Series]
DfSrsVar = TypeVar("DfSrsVar", pd.DataFrame, pd.Series)

__all__ = ["TsOperator"]

N_SNAPSHOTS = 4803


class TsOperator:
    def __init__(self, fieldtype: Type[Field]):
        self.fieldtype = fieldtype
        self._join_()

    def _accumulate(
        self,
        x: Field[D1],
        n: int,
        op_name: str,
        default: Union[Field[D1], None] = None,
        method: str = "back",
    ) -> Union[pd.DataFrame, int]:
        if op_name == "":
            raise ValueError("op_name cannot be specified as ''")

        if op_name not in self._op_count:
            self._op_count[op_name] = 0
        self._op_count[op_name] += 1
        _count = self._op_count[op_name]

        if (op_name + "_row", _count) not in self.__cache__:
            if method in ["back", "forward"]:
                fld = self.fieldtype(np.nan, timestamps=range(n), tickers=x.tickers)
                if default is not None:
                    fld.fill(default)
                self.__cache__[(op_name, _count)] = fld
            self.__cache__[(op_name + "_row", _count)] = 0

        if method == "back":
            fld: Field = self.__cache__[(op_name, _count)]
            fld = fld.shift(-1)
            fld.insert(fld.shape[0] - 1, x)
            self.__cache__[(op_name, _count)] = fld
            return fld
        elif method == "forward":
            fld: Field = self.__cache__[(op_name, _count)]
            _row: int = self.__cache__[(op_name + "_row", _count)]
            fld.iloc[_row] = x
            self.__cache__[(op_name + "_row", _count)] = _row + 1
            self.__cache__[(op_name, _count)] = fld
            return fld
        elif method == "increasing":
            _row: int = self.__cache__[(op_name + "_row", _count)]
            self.__cache__[(op_name + "_row", _count)] = _row + 1
            return _row

    def _save(self, x: Any, f_name: str):
        if f_name + "_save" not in self._op_count:
            self._op_count[f_name + "_save"] = 0
        self._op_count[f_name + "_save"] += 1
        _count = self._op_count[f_name + "_save"]

        self.__cache__[(f_name + "_save", _count)] = x

    def _load(self, f_name: str, default: Any = None) -> Any:
        if f_name + "_load" not in self._op_count:
            self._op_count[f_name + "_load"] = 0
        self._op_count[f_name + "_load"] += 1
        _count = self._op_count[f_name + "_load"]

        if (f_name + "_save", _count) not in self.__cache__:
            self._save(default, f_name)
        return self.__cache__[(f_name + "_save", _count)]

    def _reset_(self):
        for op in self._op_count:
            self._op_count[op] = 0

    def _join_(self):
        self._op_count: Dict[str, int] = {}
        for op in self._get_op_list():
            self._op_count[op] = 0
            self.__cache__: Dict[Tuple[str, int], Any] = {}

    @classmethod
    def _get_op_list(cls) -> List[str]:
        op_list: List[str] = []
        for i in dir(cls):
            if i[0] != "_" and i not in ["_get_op_list", cls.__name__]:
                op_list.append(i)
        return op_list
