"""
Contains the typing classes: _NeverInstantiateMeta, _NeverInstantiateMeta, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""

from typing import ClassVar, Optional


class _NeverInstantiateMeta(type):
    use_instead: ClassVar[Optional[str]] = None

    def __call__(cls, *args, **kwargs):
        use_instead_hint = f"; use {cls.use_instead} instead" if cls.use_instead else ""
        raise TypeError(f"type {cls.__name__} cannot be instantiated{use_instead_hint}")


class _NeverInstantiate(metaclass=_NeverInstantiateMeta):
    ...
