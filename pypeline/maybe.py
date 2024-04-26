from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable

from pypeline import pipeline, result


class AsyncMaybe[_TValue](ABC): ...


@dataclass(slots=True)
class AsyncSome[_TValue](AsyncMaybe[_TValue]): ...


@dataclass(slots=True)
class AsyncEmpty(AsyncMaybe[Any]): ...


class Maybe[_TValue](ABC):
    @staticmethod
    def some(value: _TValue) -> Maybe[_TValue]:
        return Some(value)

    @staticmethod
    def empty() -> Maybe[_TValue]:
        return Empty()

    @staticmethod
    def from_optional(value: _TValue | None) -> Maybe[_TValue]:
        if value is None:
            return _Empty

        return Some(value)

    @staticmethod
    def safe[**_ParamSpec](
        func: Callable[_ParamSpec, _TValue | None],
    ) -> Callable[_ParamSpec, Maybe[_TValue]]:
        def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
            if (res := func(*args, **kwargs)) is None:
                return Maybe[_TValue].empty()

            return Maybe[_TValue].some(res)

        return _safe

    def is_some(self) -> bool:
        return isinstance(self, Some)

    def is_empty(self) -> bool:
        return isinstance(self, Empty)

    def unwrap(self) -> _TValue:
        if not isinstance(self, Some):
            raise ValueError("is empty")

        return self.value

    def unwrap_or(self, other: _TValue | Callable[[], _TValue]) -> _TValue:
        if not isinstance(self, Some):
            return other() if isinstance(other, Callable) else other  # type: ignore

        return self.value

    def unwrap_as_optional(self) -> _TValue | None:
        if not isinstance(self, Some):
            return None

        return self.value

    def unwrap_as_result(self) -> result.Result[_TValue, Exception]:
        if not isinstance(self, Some):
            return result.Result[_TValue, Exception].err(ValueError("is empty"))

        return result.Result[_TValue, Exception].ok(self.value)

    def unwrap_as_result_or(self, other: _TValue | Callable[[], _TValue]):
        if not isinstance(self, Some):
            return result.Result[_TValue, Exception].ok(
                other() if isinstance(other, Callable) else other  # type: ignore
            )

        return result.Result[_TValue, Exception].ok(self.value)

    def unwrap_as_pipeline(self):
        if not isinstance(self, Some):
            raise ValueError("is empty")

        return pipeline.Pipeline(self.value)

    def unwrap_as_pipeline_optional(self):
        if not isinstance(self, Some):
            return pipeline.Pipeline[_TValue | None](None)

        return pipeline.Pipeline[_TValue | None](self.value)

    def unwrap_as_pipeline_or(self, other: _TValue | Callable[[], _TValue]):
        if not isinstance(self, Some):
            return pipeline.Pipeline[_TValue](
                other() if isinstance(other, Callable) else other  # type: ignore
            )

        return pipeline.Pipeline(self.value)

    def map(self): ...

    def then(self): ...


@dataclass(slots=True)
class Some[_TValue](Maybe[_TValue]):
    value: _TValue


@dataclass(slots=True)
class Empty(Maybe[Any]): ...


_Empty = Empty()
