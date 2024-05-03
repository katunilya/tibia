from __future__ import annotations

import functools
from abc import ABC
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, cast

from pypeline import pipeline, result


@dataclass(slots=True)
class AsyncMaybe[_TValue](ABC):
    value: Awaitable[Maybe[_TValue]]

    @staticmethod
    def safe[**_ParamSpec](
        func: Callable[_ParamSpec, Awaitable[_TValue | None]],
    ) -> Callable[_ParamSpec, AsyncMaybe[_TValue]]:
        def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
            async def __safe():
                result = await func(*args, **kwargs)
                if result is None:
                    return Maybe[_TValue].empty()

                return Maybe[_TValue].some(result)

            return AsyncMaybe[_TValue](__safe())

        return _safe

    async def unwrap(self):
        return (await self.value).unwrap()

    async def unwrap_or(self, other: _TValue | Callable[[], _TValue]):
        return (await self.value).unwrap_or(other)

    async def unwrap_as_optional(self):
        return (await self.value).unwrap_as_optional()

    def unwrap_as_pipeline(self):
        return pipeline.AsyncPipeline(self.unwrap())

    def unwrap_as_pipeline_or(self, other: _TValue | Callable[[], _TValue]):
        return pipeline.AsyncPipeline(self.unwrap_or(other))

    def unwrap_as_result(self):
        async def _unwrap_as_result():
            return (await self.value).unwrap_as_result()

        return result.AsyncResult(_unwrap_as_result())

    def unwrap_as_result_or(self, other: _TValue | Callable[[], _TValue]):
        async def _unwrap_as_result_or():
            return (await self.value).unwrap_as_result_or(other)

        return result.AsyncResult(_unwrap_as_result_or())

    def map[_TResult](self, func: Callable[[_TValue], _TResult]):
        async def _map():
            return (await self.value).map(func)

        return AsyncMaybe(_map())

    def then[_TResult](
        self, func: Callable[[_TValue], _TResult]
    ) -> Awaitable[_TResult]:
        async def _then():
            return (await self.value).then(func)

        return _then()

    def then_or[_TResult](
        self,
        func: Callable[[_TValue], _TResult],
        other: _TResult | Callable[[], _TResult],
    ) -> Awaitable[_TResult]:
        async def _then_or():
            return (await self.value).then_or(func, other)

        return _then_or()

    def map_async[_TResult](self, func: Callable[[_TValue], Awaitable[_TResult]]):
        async def _map_async():
            maybe = await self.value
            if isinstance(maybe, Some):
                return Maybe[_TResult].some(await func(maybe.value))

            raise ValueError("is empty")

        return AsyncMaybe(_map_async())

    def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> Awaitable[_TResult]:
        async def _then_async():
            return await func((await self.value).unwrap())

        return _then_async()

    def then_or_async[_TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> Awaitable[_TResult]:
        async def _then_or_async():
            maybe = await self.value
            if isinstance(maybe, Some):
                return await func(maybe.value)

            return cast(_TResult, other() if isinstance(other, Callable) else other)

        return _then_or_async()


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
            return cast(_TValue, other() if isinstance(other, Callable) else other)

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
                cast(_TValue, other() if isinstance(other, Callable) else other)
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
        _value = (
            self.value
            if isinstance(self, Some)
            else cast(_TValue, other() if isinstance(other, Callable) else other)
        )
        return pipeline.Pipeline(_value)

    def map[_TResult](self, func: Callable[[_TValue], _TResult]):
        if isinstance(self, Some):
            return Maybe[_TResult].some(func(self.value))

        return cast(Maybe[_TResult], self)

    def then[_TResult](self, func: Callable[[_TValue], _TResult]):
        return func(self.unwrap())

    def then_or[_TResult](
        self,
        func: Callable[[_TValue], _TResult],
        other: _TResult | Callable[[], _TResult],
    ):
        if isinstance(self, Some):
            return func(self.value)

        return cast(_TResult, other() if isinstance(other, Callable) else other)

    def map_async[_TResult](self, func: Callable[[_TValue], Awaitable[_TResult]]):
        async def _map_async():
            if isinstance(self, Some):
                return Maybe[_TResult].some(await func(self.value))

            return cast(Maybe[_TResult], self)

        return AsyncMaybe(_map_async())

    def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> Awaitable[_TResult]:
        async def _then_async():
            if isinstance(self, Some):
                return await func(self.value)

            raise ValueError("is empty")

        return _then_async()

    def then_or_async[_TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> Awaitable[_TResult]:
        async def _then_or_async():
            if isinstance(self, Some):
                return await func(self.value)

            return cast(_TResult, other() if isinstance(other, Callable) else other)

        return _then_or_async()


@dataclass(slots=True)
class Some[_TValue](Maybe[_TValue]):
    value: _TValue


@dataclass(slots=True)
class Empty(Maybe[Any]): ...


_Empty = Empty()


def safe[**_ParamSpec, _TValue](
    func: Callable[_ParamSpec, _TValue | None],
) -> Callable[_ParamSpec, Maybe[_TValue]]:
    @functools.wraps(func)
    def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs) -> Maybe[_TValue]:
        result = func(*args, **kwargs)
        if result is None:
            return Maybe[_TValue].empty()

        return Maybe[_TValue].some(result)

    return _safe  # type: ignore


def safe_async[**_ParamSpec, _TValue](
    func: Callable[_ParamSpec, Awaitable[_TValue | None]],
) -> Callable[_ParamSpec, AsyncMaybe[_TValue]]:
    @functools.wraps(func)
    def _safe(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs) -> AsyncMaybe[_TValue]:
        async def __safe():
            result = await func(*args, **kwargs)
            if result is None:
                return Maybe[_TValue].empty()

            return Maybe[_TValue].some(result)

        return AsyncMaybe(__safe())

    return _safe  # type: ignore
