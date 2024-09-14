from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Concatenate, Type

from tibia.pipeline import Pipeline


class Maybe[_TValue](ABC):
    @staticmethod
    def from_optional[_TInputValue](value: _TInputValue | None) -> Maybe[_TInputValue]:
        return Some(value) if value is not None else _Empty

    @staticmethod
    def from_value[_TInputValue](value: _TInputValue) -> Maybe[_TInputValue]:
        return Some(value)

    def is_some(self) -> bool:
        return isinstance(self, Some)

    def is_empty(self) -> bool:
        return isinstance(self, Empty)

    def unwrap(self) -> _TValue:
        if isinstance(self, Some):
            return self._value

        raise ValueError("Maybe is Empty")

    def unwrap_as_optional(self) -> _TValue | None:
        return self._value if isinstance(self, Some) else None

    def unwrap_or(self, other: _TValue) -> _TValue:
        return self._value if isinstance(self, Some) else other

    def unwrap_or_compute[**_ParamSpec](
        self,
        func: Callable[_ParamSpec, _TValue],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TValue:
        return self._value if isinstance(self, Some) else func(*args, **kwargs)

    def unwrap_as_pipeline(self) -> Pipeline[_TValue]:
        return Pipeline(self.unwrap())

    def unwrap_or_as_pipeline(self, other: _TValue) -> Pipeline[_TValue]:
        return Pipeline(self.unwrap_or(other))

    def unwrap_or_compute_as_pipeline[**_ParamSpec](
        self,
        func: Callable[_ParamSpec, _TValue],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Pipeline[_TValue]:
        return Pipeline(self.unwrap_or_compute(func, *args, **kwargs))

    def map[_TReturn, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Maybe[_TReturn]:
        if isinstance(self, Some):
            return Some(func(self._value, *args, **kwargs))

        return _Empty

    def map_safe[_TReturn, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn | None],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Maybe[_TReturn]:
        if (
            isinstance(self, Some)
            and (value := func(self._value, *args, **kwargs)) is not None
        ):
            return Some(value)

        return _Empty

    def apply[_TReturn, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], Maybe[_TReturn]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Maybe[_TReturn]:
        if isinstance(self, Some):
            return func(self._value, *args, **kwargs)

        return _Empty

    def recover_with(self, value: _TValue) -> Maybe[_TValue]:
        return self if isinstance(self, Some) else Some(value)

    def recover_with_compute[**_ParamSpec](
        self,
        func: Callable[_ParamSpec, _TValue],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Maybe[_TValue]:
        return self if isinstance(self, Some) else Some(func(*args, **kwargs))


@dataclass(slots=True)
class Some[_TValue](Maybe[_TValue]):
    _value: _TValue

    def as_maybe(self) -> Maybe[_TValue]:
        return self  # pragma: no cover


@dataclass(slots=True)
class Empty(Maybe[Any]):
    def as_maybe[_TValue](self, _: Type[_TValue]) -> Maybe[_TValue]:
        return self  # pragma: no cover


_Empty = Empty()
