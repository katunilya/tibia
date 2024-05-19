from __future__ import annotations

import functools
from abc import ABC
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Type, cast

from pypeline import pipeline, result


@dataclass(slots=True)
class AsyncMaybe[_TValue](ABC):
    value: Awaitable[Maybe[_TValue]]

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
                return Some(await func(maybe.unwrap()))

            return cast(Maybe[_TResult], maybe)

        return AsyncMaybe(_map_async())

    async def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> _TResult:
        return await func((await self.value).unwrap())

    async def then_or_async[_TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> _TResult:
        maybe = await self.value
        if not isinstance(maybe, Some):
            return cast(_TResult, other() if isinstance(other, Callable) else other)

        return await func(maybe.value)


class Maybe[_TValue](ABC):
    def is_some(self) -> bool:
        return isinstance(self, Some)

    def is_empty(self) -> bool:
        return isinstance(self, Empty)

    def unwrap(self) -> _TValue:
        if not isinstance(self, Some):
            raise ValueError("empty")

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
            return result.Err(ValueError("empty"))

        return result.Ok(self.value)

    def unwrap_as_result_or(self, other: _TValue | Callable[[], _TValue]):
        if not isinstance(self, Some):
            _other = cast(_TValue, other() if isinstance(other, Callable) else other)
            return result.Ok(_other).as_result(Exception)

        return result.Ok(self.value).as_result(Exception)

    def unwrap_as_pipeline(self):
        if not isinstance(self, Some):
            raise ValueError("empty")

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
        if not isinstance(self, Some):
            return cast(Maybe[_TResult], self)

        return Some(func(self.value)).as_maybe()

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
            if not isinstance(self, Some):
                return cast(Maybe[_TResult], self)

            return Some(await func(self.value)).as_maybe()

        return AsyncMaybe(_map_async())

    async def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> _TResult:
        if isinstance(self, Some):
            return await func(self.value)

        raise ValueError("empty")

    async def then_or_async[_TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        other: _TResult | Callable[[], _TResult],
    ) -> _TResult:
        if isinstance(self, Some):
            return await func(self.value)

        return cast(_TResult, other() if isinstance(other, Callable) else other)


@dataclass(slots=True)
class Some[_TValue](Maybe[_TValue]):
    value: _TValue

    def as_maybe(self) -> Maybe[_TValue]:
        return self


@dataclass(slots=True)
class Empty(Maybe[Any]):
    def as_maybe[_TValue](self, _: Type[_TValue]) -> Maybe[_TValue]:
        return self


_Empty = Empty()


def maybe_returns[**_ParamSpec, _TValue](
    func: Callable[_ParamSpec, _TValue | None],
) -> Callable[_ParamSpec, Maybe[_TValue]]:
    @functools.wraps(func)
    def _maybe_returns(
        *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
    ) -> Maybe[_TValue]:
        result = func(*args, **kwargs)
        if result is None:
            return _Empty

        return Some(result)

    return _maybe_returns  # type: ignore


def maybe_returns_async[**_ParamSpec, _TValue](
    func: Callable[_ParamSpec, Awaitable[_TValue | None]],
) -> Callable[_ParamSpec, AsyncMaybe[_TValue]]:
    @functools.wraps(func)
    def _maybe_returns_async(
        *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
    ) -> AsyncMaybe[_TValue]:
        async def __maybe_returns_async():
            result = await func(*args, **kwargs)
            if result is None:
                return _Empty

            return Some(result)

        return AsyncMaybe(__maybe_returns_async())

    return _maybe_returns_async  # type: ignore


def maybe_from_optional[_TValue](value: _TValue | None) -> Maybe[_TValue]:
    if value is None:
        return _Empty
    return Some(value)


def maybe_unwrap[_TValue](maybe: Maybe[_TValue]) -> _TValue:
    return maybe.unwrap()
