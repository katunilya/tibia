from typing import Any, Callable, Type


def as_type[_TType](target_type: Type[_TType]) -> Callable[[Any], _TType]:
    def _as_type(value: Any) -> _TType:
        if not isinstance(value, target_type):
            raise ValueError(f"cannot cast to {target_type.__name__}")

        return value

    return _as_type
