from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Concatenate


@dataclass(slots=True)
class AsyncPipeline[_TValue]:
    _value: Awaitable[_TValue]

    async def unwrap(self) -> _TValue:
        return await self._value

    def map[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TReturn]:
        async def _map():
            return func(await self._value, *args, **kwargs)

        return AsyncPipeline(_map())

    async def apply[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TReturn:
        return func(await self._value, *args, **kwargs)

    def map_async[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[_TReturn]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TReturn]:
        async def _map():
            return await func(await self._value, *args, **kwargs)

        return AsyncPipeline(_map())

    async def apply_async[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[_TReturn]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TReturn:
        return await func(await self._value, *args, **kwargs)


@dataclass(slots=True)
class Pipeline[_TValue]:
    _value: _TValue

    def unwrap(self) -> _TValue:
        return self._value

    def map[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Pipeline[_TReturn]:
        return Pipeline(func(self._value, *args, **kwargs))

    def apply[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TReturn:
        return func(self._value, *args, **kwargs)

    def map_async[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[_TReturn]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> AsyncPipeline[_TReturn]:
        return AsyncPipeline(func(self._value, *args, **kwargs))

    async def apply_async[**_ParamSpec, _TReturn](
        self,
        func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[_TReturn]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TReturn:
        return await func(self._value, *args, **kwargs)
