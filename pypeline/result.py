from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, cast

from pypeline import maybe, pipeline
from pypeline.utils import async_identity


@dataclass(slots=True)
class AsyncResult[_TOk, _TErr]:
    value: Awaitable[Result[_TOk, _TErr]]  # type: ignore

    @staticmethod
    def safe[**_ParamSpec](
        func: Callable[_ParamSpec, Awaitable[_TOk]],
    ) -> Callable[_ParamSpec, AsyncResult[_TOk, Exception]]:
        def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
            async def __safe() -> Result[_TOk, Exception]:
                try:
                    return Ok(func(*args, **kwargs))
                except Exception as exc:
                    return Err(exc)

            return AsyncResult(__safe())

        return _safe

    async def unwrap(self):
        return (await self.value).unwrap()

    async def unwrap_or(self, other: Callable[[], _TOk]):
        return (await self.value).unwrap_or(other)

    def unwrap_as_pipeline(self):
        return pipeline.AsyncPipeline(self.unwrap())

    def unwrap_as_pipeline_or(self, other: Callable[[], _TOk]):
        return pipeline.AsyncPipeline(self.unwrap_or(other))

    # TODO impl unwrap_as_maybe; BLOCK impl AsyncMaybe
    # TODO impl unwrap_as_maybe_or; BLOCK impl AsyncMaybe

    def map[_TResult](
        self, func: Callable[[_TOk], _TResult]
    ) -> AsyncResult[_TResult, _TErr]:
        async def _map():
            return (await self.value).map(func)

        return AsyncResult(_map())

    def map_async[_TResult](
        self, func: Callable[[_TOk], Awaitable[_TResult]]
    ) -> AsyncResult[_TResult, _TErr]:
        async def _map_async() -> Result[_TResult, _TErr]:
            result = await self.value

            if isinstance(result, Ok):
                return Ok(await func(result.value))
            return result  # type: ignore

        return AsyncResult(_map_async())

    def then[_TResult](self, func: Callable[[_TOk], _TResult]) -> Awaitable[_TResult]:
        async def _then():
            return (await self.value).then(func)

        return _then()

    def then_async[_TResult](
        self, func: Callable[[_TOk], Awaitable[_TResult]]
    ) -> Awaitable[_TResult]:
        async def _then_async():
            return await (await self.value).then_async(func)

        return _then_async()

    def then_or[_TResult](
        self, func: Callable[[_TOk], _TResult], other: _TResult | Callable[[], _TResult]
    ) -> Awaitable[_TResult]:
        async def _then_or():
            return (await self.value).then_or(func, other)

        return _then_or()

    def then_or_async[_TResult](
        self,
        func: Callable[[_TOk], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> Awaitable[_TResult]:
        async def _then_or_async():
            return await (await self.value).then_or_async(func, other)

        return _then_or_async()


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

    def map[_TResult](
        self, func: Callable[[_TOk], _TResult]
    ) -> Result[_TResult, _TErr]:
        if isinstance(self, Ok):
            return Ok(func(self.value))

        return self  # type: ignore

    def map_async[_TResult](
        self, func: Callable[[_TOk], Awaitable[_TResult]]
    ) -> AsyncResult[_TResult, _TErr]:
        async def _map_async() -> Result[_TResult, _TErr]:
            if isinstance(self, Ok):
                return Ok(await func(self.value))

            return self  # type: ignore

        return AsyncResult(_map_async())

    def then[_TResult](self, func: Callable[[_TOk], _TResult]) -> _TResult:
        value = self.unwrap()
        return func(value)

    def then_async[_TResult](
        self, func: Callable[[_TOk], Awaitable[_TResult]]
    ) -> Awaitable[_TResult]:
        value = self.unwrap()
        return func(value)

    def then_or[_TResult](
        self, func: Callable[[_TOk], _TResult], other: _TResult | Callable[[], _TResult]
    ) -> _TResult:
        return self.map(func).unwrap_or(other)

    def then_or_async[_TResult](
        self,
        func: Callable[[_TOk], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> Awaitable[_TResult]:
        if isinstance(self, Ok):
            return func(self.value)

        _other = cast(_TResult, other() if isinstance(other, Callable) else other)

        return async_identity(_other)


@dataclass(slots=True)
class Ok[_TOk](Result[_TOk, Any]):
    value: _TOk


@dataclass(slots=True)
class Err[_TErr](Result[Any, _TErr]):
    value: _TErr
