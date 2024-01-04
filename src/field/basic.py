"""
Contains a pandas implemention of the abstract class Field.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from .abstract import Field

__all__ = ["PandasField"]


class PandasField(Field):
    pass
