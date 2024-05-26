from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(slots=True)
class AsyncCompose[**_ParamSpec, _TResult]:
    _value: Callable[_ParamSpec, Awaitable[_TResult]]

    async def __call__(
        self,
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TResult:
        return await self._value(*args, **kwargs)

    def then[_TNewResult](
        self, func: Callable[[_TResult], _TNewResult]
    ) -> AsyncCompose[_ParamSpec, _TNewResult]:
        async def _then(
            *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
        ) -> _TNewResult:
            return func(await self._value(*args, **kwargs))

        return AsyncCompose(_then)

    def then_async[_TNewResult](
        self, func: Callable[[_TResult], Awaitable[_TNewResult]]
    ) -> AsyncCompose[_ParamSpec, _TNewResult]:
        async def _then_async(
            *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
        ) -> _TNewResult:
            return await func(await self._value(*args, **kwargs))

        return AsyncCompose(_then_async)


@dataclass(slots=True)
class Compose[**_ParamSpec, _TResult]:
    _value: Callable[_ParamSpec, _TResult]

    def __call__(self, *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs) -> _TResult:
        return self._value(*args, **kwargs)

    def then[_TNewResult](
        self, func: Callable[[_TResult], _TNewResult]
    ) -> Compose[_ParamSpec, _TNewResult]:
        def _then(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs) -> _TNewResult:
            return func(self._value(*args, **kwargs))

        return Compose(_then)

    def then_async[_TNewResult](
        self, func: Callable[[_TResult], Awaitable[_TNewResult]]
    ) -> AsyncCompose[_ParamSpec, _TNewResult]:
        async def _then_async(
            *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
        ) -> _TNewResult:
            return await func(self._value(*args, **kwargs))

        return AsyncCompose(_then_async)
