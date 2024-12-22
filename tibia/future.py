from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate


@dataclass(slots=True)
class Future[T]:
    _internal: Awaitable[T]

    def __await__(self):
        return self._internal.__await__()

    def unwrap(self) -> Awaitable[T]:
        return self._internal

    def map[**P, R](
        self,
        func: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        @functools.wraps(func)
        async def _map(
            value: Awaitable[T],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            return func(await value, *args, **kwargs)

        return Future(_map(self._internal, *args, **kwargs))

    def map_async[**P, R](
        self,
        func: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        @functools.wraps(func)
        async def _map_async(
            value: Awaitable[T],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            return await func(await value, *args, **kwargs)

        return Future(_map_async(self._internal, *args, **kwargs))

    def inspect[**P](
        self,
        func: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[T]:
        @functools.wraps(func)
        async def _inspect(
            value: Awaitable[T],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            _value = await value
            func(_value, *args, **kwargs)
            return _value

        return Future(_inspect(self._internal, *args, **kwargs))

    def inspect_async[**P](
        self,
        func: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[T]:
        @functools.wraps(func)
        async def _inspect_async(
            value: Awaitable[T],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            _value = await value
            await func(_value, *args, **kwargs)
            return _value

        return Future(_inspect_async(self._internal, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, Future[R]]:
        @functools.wraps(func)
        def _wraps(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Future[R]:
            return Future(func(*args, **kwargs))

        return _wraps
