"""
Contains ABCs with Validators: ABCV, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Callable, TypeVar

from typing_extensions import Self

F = TypeVar("F", bound=Callable)

__all__ = [
    "ABCV",
    "ABCVMeta",
    "abstractmethodval",
    "method_validator",
    "add_method_validator",
    "MethodImplementionError",
]


def abstractmethodval(method: F) -> F:
    """
    A decorator indicating abstract methods. Differences to `abc.abstractmethod()`
    that a new attribute 'val' is added to the method, which can be used to mark
    the validator of the method.

    Parameters
    ----------
    method : C
        Abstract method.

    Returns
    -------
    C
        Decorated method with a new attribute 'val'.

    """
    f = abstractmethod(method)
    setattr(f, "val", method_validator(method))
    return f


def method_validator(method: Callable) -> Callable[[F], F]:
    """
    Mark the decorated function as a validator of the specified abstract method.
    If the abstract method is implemented by subclasses, the validator should
    check the return types of the implemented method, and throw a
    `MethodImplementionError` if the types aren't correct.

    Parameters
    ----------
    method : Callable
        The abstract method to be implemented by subclasses.

    Returns
    -------
    Callable[[C], C]
        A decorator to mark the validator.

    """

    def decorator(validator: F) -> F:
        @wraps(validator)
        def wrapper(self: object, *args, **kwargs) -> Any:
            try:
                return validator(self, *args, **kwargs)
            except MethodImplementionError as e:
                raise e << (
                    f"This may be caused by a bad implemention of the method "
                    f"{method.__name__}() in {type(self)}."
                )

        setattr(wrapper, "__validator_of__", method.__name__)

        return wrapper

    return decorator


def add_method_validator(validator: Callable[[object, Any], None]) -> Callable[[F], F]:
    """
    Add a validator to the decorated method during runtime.

    Parameters
    ----------
    validator : Callable[[object, Any], None]
        A method validator, see `method_validator()`.

    Returns
    -------
    Callable[[C], C]
        A decorator that adds the validator to a method.

    """

    def decorator(method: F) -> F:
        @wraps(method)
        def wrapper(self: object, *args, **kwargs) -> Any:
            result = method(self, *args, **kwargs)
            validator(self, result)
            return result

        return wrapper

    return decorator


class ABCVMeta(ABCMeta):
    """Metaclass of ABCVs."""

    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if cls.__abstractmethods__:
            return
        if issubclass(cls, ABCV) and cls._trust_mode:
            return
        for f in (getattr(cls, x) for x in dir(cls)):
            if hasattr(f, "__validator_of__"):
                m: str = getattr(f, "__validator_of__")
                setattr(cls, m, add_method_validator(f)(getattr(cls, m)))


class ABCV(metaclass=ABCVMeta):
    """
    ABCVs stands for Abstract Base Classes with Validators.

    """

    _trust_mode: bool = False  # Set this to True in a subclass if the implementions
    # of all its methods can be fully trusted (NOT recommended).


class MethodImplementionError(Exception):
    """
    Raised when the implemention of a method returns unexpected results.

    """

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    def __lshift__(self, msg: str) -> Self:
        self.args = (self.args[0] + "\n" + msg,)
        return self
