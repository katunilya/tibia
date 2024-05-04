from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(slots=True)
class AsyncPipeline[_TValue]:
    value: Awaitable[_TValue]

    async def unwrap(self) -> _TValue:
        return await self.value

    def map[_TResult](
        self, func: Callable[[_TValue], _TResult]
    ) -> AsyncPipeline[_TResult]:
        async def _map(value: Awaitable[_TValue]) -> _TResult:
            return func(await value)

        return AsyncPipeline(_map(self.value))

    def map_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> AsyncPipeline[_TResult]:
        async def _map_async(value: Awaitable[_TValue]) -> _TResult:
            return await func(await value)

        return AsyncPipeline(_map_async(self.value))

    async def then[_TResult](self, func: Callable[[_TValue], _TResult]) -> _TResult:
        return func(await self.value)

    async def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> _TResult:
        return await func(await self.value)


@dataclass(slots=True)
class Pipeline[_TValue]:
    value: _TValue

    def unwrap(self) -> _TValue:
        return self.value

    def map[_TResult](self, func: Callable[[_TValue], _TResult]) -> Pipeline[_TResult]:
        return Pipeline(func(self.value))

    def map_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> AsyncPipeline[_TResult]:
        return AsyncPipeline(func(self.value))

    def then[_TResult](self, func: Callable[[_TValue], _TResult]) -> _TResult:
        return func(self.value)

    async def then_async[_TResult](
        self, func: Callable[[_TValue], Awaitable[_TResult]]
    ) -> _TResult:
        return await func(self.value)
