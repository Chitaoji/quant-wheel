"""
Contains the abstract class: AbstractField.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar, Union, cast, final

from ._types import D0, D1, D2, Data, Field, Num

C = TypeVar("C", bound=Callable)

__all__ = ["AbstractField"]


class _AbstractFieldMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        if issubclass(cls, AbstractField):
            self = cast(AbstractField, cls.__new__(cls, *args, **kwargs))
            self.__init__(*args, **kwargs)
            self._init_valitator()
            self.shift = impl_validate(self._shift_validator)(self.shift)
            self.setrow = impl_validate(self._setrow_validator)(self.setrow)
            return self
        else:
            raise TypeError(
                "_AbstractFieldMeta must be a metaclass of AbstractField or its"
                f" subclasses, but the class was {cls}"
            )


def impl_validator(method: Callable) -> Callable[[C], C]:
    """
    Mark the decorated function as a validator of the specified abstract
    method. If the method is implemented by subclasses, the validator
    should check the return types of the new method, and throw a
    MethodImplementionError if the types aren't correct.

    Parameters
    ----------
    method : Callable
        The method to be implemented by subclasses.

    Returns
    -------
    Callable[[C], C]
        A decorator to mark the validator.

    """

    def decorator(func: C) -> C:
        @wraps(func)
        def wrapper(self: object, *args, **kwargs) -> Any:
            try:
                return func(self, *args, **kwargs)
            except MethodImplementionError as e:
                e.add_note(
                    f"This may be caused by a bad implemention of the method "
                    f"{method.__name__}() in {type(self)}."
                )
                raise e

        return wrapper

    return decorator


def impl_validate(validator: Callable) -> Callable[[C], C]:
    """
    Validate the decorated function with the specified validator.

    Parameters
    ----------
    validator : Callable
        A validator of method.

    Returns
    -------
    Callable[[C], C]
        A decorator to validate the methods.

    """

    def decorator(func: C) -> C:
        @wraps(func)
        def wrapper(self: object, *args, **kwargs) -> Any:
            result = func(self, *args, **kwargs)
            validator(*result)
            return result

        return wrapper

    return decorator


class AbstractField(metaclass=_AbstractFieldMeta):
    """Abstract field type."""

    @abstractmethod
    def __init__(
        self,
        data: Any,
        tickers: Optional[list] = None,
        timestamps: Optional[list] = None,
    ) -> None:
        """Initialzing. See Field.__init__()."""

    @abstractmethod
    def shift(self, n: int = 1) -> None:
        """Method for D2 only. See Field.shift()."""

    @abstractmethod
    def setrow(self, n: int, value: Union[Num, "Field[D1]"]) -> None:
        """Method for D2 only. See Field.setrow()."""

    @final
    @impl_validator(__init__)
    def _init_valitator(self) -> None:
        data = getattr(self, "data")
        if isinstance(data, D0):
            dim = D0
            self.__check_attr_is_none("tickers", dim)
            self.__check_attr_is_none("timestamps", dim)
        elif isinstance(data, D1):
            dim = D1
            self.__check_attr_is_none("timestamps", dim)
        elif isinstance(data, D2):
            dim = D2
        else:
            raise MethodImplementionError(
                f"attribute 'data' must be of type D0, D1 or D2, got {type(data)}."
            )
        setattr(self, "dim", dim)

    @final
    @impl_validator(shift)
    def _shift_validator(self) -> None:
        pass

    @final
    @impl_validator(setrow)
    def _setrow_validator(self) -> None:
        pass

    def __check_attr_is_none(self, __name: str, __dim: Type[Data]) -> None:
        if (v := getattr(self, __name)) is not None:
            raise MethodImplementionError(
                f"attribute '{__name}' must be None when dim = {__dim.__name__}, got {v}."
            )


class MethodImplementionError(Exception):
    """
    Raised when the implemention of a method returns unexpected results.

    """

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.cls: type = None  # Where the method is implemented.
