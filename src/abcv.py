"""
Contains ABCs with Validators: ABCV, etc.

NOTE: this module is private. All functions and objects are available in the main
`quant_wheel` namespace - use that instead.

"""
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Callable, Type, TypeVar

from typing_extensions import Self

F = TypeVar("F", bound=Callable)

__all__ = [
    "ABCV",
    "ABCVMeta",
    "abstractmethodval",
    "before_validator",
    "after_validator",
    "is_validator",
    "add_validator",
    "MethodCallError",
    "MethodImplementionError",
]


BEFORE_TAG = "__validator_before__"
AFTER_TAG = "__validator_after__"


def abstractmethodval(method: F) -> F:
    """
    A decorator indicating abstract methods. Differences to `abc.abstractmethod()`
    that two new attributes 'before' and 'after' are added to the method, which
    can be used to mark the before-validator and after-validator of it.

    Parameters
    ----------
    method : F
        Abstract method.

    Returns
    -------
    F
        Decorated method with new attributes 'before' and 'after'.

    """
    f = abstractmethod(method)
    setattr(f, "before", before_validator(method))
    setattr(f, "after", after_validator(method))
    return f


def before_validator(method: Callable) -> Callable[[F], F]:
    """
    Mark the decorated function as a before-validator of the specified abstract
    method. If the abstract method is implemented by subclasses, the validator
    should check the inputs of the implemented method, and throw a
    `MethodCallError` if the inputs are illegal.

    Parameters
    ----------
    method : Callable
        The abstract method to be implemented by subclasses.

    Returns
    -------
    Callable[[F], F]
        A decorator to mark the validator.

    """

    def decorator(func: F) -> F:
        __tag_update(func, BEFORE_TAG, [method.__name__])
        return func

    return decorator


def after_validator(method: Callable) -> Callable[[F], F]:
    """
    Mark the decorated function as an after-validator of the specified abstract
    method. If the abstract method is implemented by subclasses, the validator
    should check the returns of the implemented method, and throw a
    `MethodImplementionError` if the returns are illegal.

    Parameters
    ----------
    method : Callable
        The abstract method to be implemented by subclasses.

    Returns
    -------
    Callable[[F], F]
        A decorator to mark the validator.

    """

    def decorator(func: F) -> F:
        __tag_update(func, AFTER_TAG, [method.__name__])
        return func

    return decorator


def __tag_update(func: Callable, tag: str, values: list) -> None:
    if not is_validator(func):
        setattr(func, BEFORE_TAG, frozenset())
        setattr(func, AFTER_TAG, frozenset())
    setattr(func, tag, getattr(func, tag) | frozenset(values))


def is_validator(func: Callable) -> bool:
    """
    Check whether a function object is a validator or not.

    Parameters
    ----------
    func : Callable
        Function object.

    Returns
    -------
    bool
        Whether the function object is a validator or not.

    """
    return hasattr(func, BEFORE_TAG) and hasattr(func, AFTER_TAG)


def add_validator(validator: Callable[[object, Any], None]) -> Callable[[F], F]:
    """
    Add a validator to the decorated method during runtime.

    Parameters
    ----------
    validator : Callable[[object, Any], None]
        A method validator, see `after_validator()` and `before_validator()`.

    Returns
    -------
    Callable[[F], F]
        A decorator that adds the validator to a method.

    """
    if not is_validator(validator):
        raise ValueError(f"the input is not a legal validator: {validator}")

    def decorator(method: F) -> F:
        @wraps(method)
        def wrapper(self: object, *args, **kwargs) -> Any:
            if method.__name__ in getattr(validator, BEFORE_TAG):
                __trans_before_validator(validator, method)(self, *args, **kwargs)
            result = method(self, *args, **kwargs)
            if method.__name__ in getattr(validator, AFTER_TAG):
                __trans_after_validator(validator, method)(self, result)
            return result

        return wrapper

    return decorator


def __trans_before_validator(validator: F, method: Callable) -> F:
    @wraps(validator)
    def wrapper(self: object, *args, **kwargs) -> Any:
        try:
            return validator(self, *args, **kwargs)
        except MethodCallError as e:
            raise e << (
                "This error occurs during the call of method "
                f"{method.__name__}() in {type(self)}."
            )

    return wrapper


def __trans_after_validator(validator: F, method: Callable) -> F:
    @wraps(validator)
    def wrapper(self: object, *args, **kwargs) -> Any:
        try:
            return validator(self, *args, **kwargs)
        except MethodImplementionError as e:
            raise e << (
                f"This may be caused by a bad implemention of the method "
                f"{method.__name__}() in {type(self)}."
            )

    return wrapper


class ABCVMeta(ABCMeta):
    """Metaclass of ABCVs."""

    def __init__(cls: Type["ABCV"], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if hasattr(cls, "_trust_mode") and cls._trust_mode:
            return
        if cls.__abstractmethods__:
            return
        for f in (getattr(cls, x) for x in dir(cls)):
            if is_validator(f):
                for i in getattr(f, BEFORE_TAG) | getattr(f, AFTER_TAG):
                    setattr(cls, i, add_validator(f)(getattr(cls, i)))


class ABCV(metaclass=ABCVMeta):
    """
    ABCVs stands for Abstract Base Classes with Validators.

    """

    _trust_mode: bool = False  # Set this to True in a subclass if the implementions
    # of all its methods can be fully trusted (NOT recommended).


class ABCVError(Exception):
    """
    Base class for errors related to ABCVs.

    Parameters
    ----------
    msg : str
        The error message.

    """

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    def __lshift__(self, msg: str) -> Self:
        self.args = (self.args[0] + "\n" + msg,)
        return self


class MethodCallError(ABCVError):
    """
    Raised when calling a method with wrong arguments or on an illegal instance.

    """


class MethodImplementionError(ABCVError):
    """
    Raised when the implemention of a method returns unexpected results.

    """
