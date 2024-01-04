from functools import wraps
from typing import TypeVar

F = TypeVar("F")

__all__ = ["withname"]


def withname(func: F) -> F:
    """
    Pass a function's name to itself, the wrapper will receive a new keyword
    argument `_name_`.

    Parameters
    ----------
    func : FuncVar
        An arbitrary function.

    Returns
    -------
    FuncVar
        The wrapper function.

    Raises
    ------
    TypeError
        Rased when the function got an unexpected keyword argument `_name_`,
        which is in conflict with the wrapper's keyword arguments.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "_name_" in kwargs:
            raise TypeError(
                f"`{func.__name__}` reveives unexpected keyword argument `_name_`"
            )
        else:
            kwargs["_name_"] = func.__name__
            return func(*args, **kwargs)

    return wrapper
