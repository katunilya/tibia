from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Concatenate


@dataclass(slots=True)
class AsyncPipeline[_TValue]:
    value: Awaitable[_TValue]

    async def unwrap(self) -> _TValue:
        return await self.value

    def map[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TResult]:
        async def _map(value: Awaitable[_TValue]) -> _TResult:
            return func(await value, *args, **kwargs)

        return AsyncPipeline(_map(self.value))

    def map_async[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TResult]:
        async def _map_async(value: Awaitable[_TValue]) -> _TResult:
            return await func(await value, *args, **kwargs)

        return AsyncPipeline(_map_async(self.value))

    async def then[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TResult:
        return func(await self.value, *args, **kwargs)

    async def then_async[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TResult:
        return await func(await self.value, *args, **kwargs)


@dataclass(slots=True)
class Pipeline[_TValue]:
    value: _TValue

    def unwrap(self) -> _TValue:
        return self.value

    def map[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Pipeline[_TResult]:
        return Pipeline(func(self.value, *args, **kwargs))

    def map_async[**_ParamSpec, _TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TResult]:
        return AsyncPipeline(func(self.value, *args, **kwargs))

    def then[**_ParamSpec, _TResult](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TResult:
        return func(self.value, *args, **kwargs)

    async def then_async[**_ParamSpec, _TResult](
        self,
        func: Callable[[_TValue], Awaitable[_TResult]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TResult:
        return await func(self.value, *args, **kwargs)
