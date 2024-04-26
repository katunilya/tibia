from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable

from pypeline import maybe, pipeline


class AsyncResult[_TOk, _TErr](ABC): ...


class AsyncOk: ...


class AsyncErr: ...


class Result[_TOk, _TErr](ABC):
    @staticmethod
    def ok(value: _TOk) -> Result[_TOk, _TErr]:
        return Ok(value)

    @staticmethod
    def err(value: _TErr) -> Result[_TOk, _TErr]:
        return Err(value)

    @staticmethod
    def safe[**_ParamSpec](
        func: Callable[_ParamSpec, _TOk],
    ) -> Callable[_ParamSpec, Result[_TOk, Exception]]:
        def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
            try:
                return Result[_TOk, Exception].ok(func(*args, **kwargs))
            except Exception as exc:
                return Result[_TOk, Exception].err(exc)

        return _safe

    def unwrap(self) -> _TOk:
        if not isinstance(self, Ok):
            raise ValueError("not ok", self.value)  # type: ignore

        return self.value

    def unwrap_or(self, other: _TOk | Callable[[], _TOk]) -> _TOk:
        if not isinstance(self, Ok):
            return other() if isinstance(other, Callable) else other  # type: ignore

        return self.value

    def unwrap_as_pipeline(self) -> pipeline.Pipeline[_TOk]:
        return pipeline.Pipeline(self.unwrap())

    def unwrap_as_pipeline_or(
        self, other: _TOk | Callable[[], _TOk]
    ) -> pipeline.Pipeline[_TOk]:
        return pipeline.Pipeline(self.unwrap_or(other))

    def unwrap_as_maybe(self) -> maybe.Maybe[_TOk]:
        return maybe.Some(self.unwrap())

    def unwrap_as_maybe_or(self, other: _TOk | Callable[[], _TOk]) -> maybe.Maybe[_TOk]:
        return maybe.Some(self.unwrap_or(other))


@dataclass(slots=True)
class Ok[_TOk](Result[_TOk, Any]):
    value: _TOk


@dataclass(slots=True)
class Err[_TErr](Result[Any, _TErr]):
    value: _TErr
