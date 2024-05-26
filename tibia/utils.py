from functools import wraps
from typing import Any, Callable


def identity[_TValue](value: _TValue) -> _TValue:
    return value  # pragma: no cover


async def async_identity[_TValue](value: _TValue) -> _TValue:
    return value  # pragma: no cover


def passing[_TValue](func: Callable[[_TValue], Any]) -> Callable[[_TValue], _TValue]:
    @wraps(func)
    def _passing(value: _TValue) -> _TValue:
        func(value)
        return value

    return _passing
