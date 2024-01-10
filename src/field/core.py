"""
Contains the core of field: field(), fieldtype(), etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from typing import Any, Dict, Literal, Optional, Type, Union

from ._types import Field
from .basic import PandasField

ImplName = Union[Literal["default"], Literal["pandas"]]
FieldDict: Dict[ImplName, Type[Field]] = {
    "default": PandasField,
    "pandas": PandasField,
}

__all__ = ["field", "fieldtype"]


def fieldtype(impl: Union[ImplName, Type[Field], None] = None) -> Type[Field]:
    """
    Returns an implementation type of Field, e.g. PandasField.

    Parameters
    ----------
    impl : Union[ImplName, Type[Field], None], optional
        Specifies which implementation type of Field should be used. If None,
        returns the default PandasField. By default None.

    Returns
    -------
    Type[Field]
        A Field type.

    """

    if isinstance(impl, str):
        return FieldDict[impl]
    if isinstance(impl, type):
        return impl
    return FieldDict["default"]


def field(
    data: Any,
    tickers: Optional[list] = None,
    timestamps: Optional[list] = None,
    impl: Union[ImplName, Type[Field], None] = None,
) -> Field:
    """
    Returns a Field object based on the provided data, tickers, timestamps, and
    implementation type.

    Parameters
    ----------
    data : Any
        The data that will be used to create the field.
    tickers : Optional[list], optional
        Symbols of tickers, by default None.
    timestamps : Optional[list], optional
        The timestamps associated with the data, by default None.
    impl : Optional[Literal[pandas]], optional
        Specifies the implementation type to use for the Field object, by default
        None.

    Returns
    -------
    Field
        A Field object.

    """
    return fieldtype(impl=impl)(data, tickers=tickers, timestamps=timestamps)
