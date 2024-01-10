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
            raise ValueError("the operator name cannot be specified as ''")

        if op_name not in self._op_count:
            self._op_count[op_name] = 0
        self._op_count[op_name] += 1
        _count = self._op_count[op_name]

        if (op_name + "_row", _count) not in self.__cache__:
            if method in ["back", "forward"]:
                if default is None:
                    default = np.nan
                fld = self.fieldtype(default).expand(
                    timestamps=list(range(n)), tickers=x.tickers
                )
                self.__cache__[(op_name, _count)] = fld
            self.__cache__[(op_name + "_row", _count)] = 0

        if method == "back":
            v: Field[D2] = self.__cache__[(op_name, _count)]
            v = v.shift(-1)
            v.setrow(v.shape[0] - 1, x)
            self.__cache__[(op_name, _count)] = v
            return v
        elif method == "forward":
            v: Field[D2] = self.__cache__[(op_name, _count)]
            _row: int = self.__cache__[(op_name + "_row", _count)]
            v.setrow(_row, x)
            self.__cache__[(op_name + "_row", _count)] = _row + 1
            self.__cache__[(op_name, _count)] = v
            return v
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
