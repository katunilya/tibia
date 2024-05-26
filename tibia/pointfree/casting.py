from typing import Any, Callable, Type

from tibia.maybe import Empty, Maybe, Some
from tibia.result import Err, Ok, Result


def as_type[_TType](target_type: Type[_TType]) -> Callable[[Any], _TType]:
    def _as_type(value: Any) -> _TType:
        if not isinstance(value, target_type):
            raise ValueError(f"cannot cast to {target_type.__name__}")

        return value

    return _as_type


def as_type_maybe[_TType](target_type: Type[_TType]) -> Callable[[Any], Maybe[_TType]]:
    def _as_type_maybe(value: Any) -> Maybe[_TType]:
        if not isinstance(value, target_type):
            return Empty()

        return Some(value)

    return _as_type_maybe


def as_type_result[_TType](
    target_type: Type[_TType],
) -> Callable[[Any], Result[_TType, Exception]]:
    def _as_type_result(value: Any) -> Result[_TType, Exception]:
        if not isinstance(value, target_type):
            return Err(ValueError(f"cannot cast to {target_type.__name__}"))

        return Ok(value)

    return _as_type_result
