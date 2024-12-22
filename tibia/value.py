from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate

from tibia.future import Future


@dataclass(slots=True)
class Value[T]:
    _internal: T

    def unwrap(self) -> T:
        return self._internal

    def map[**P, R](
        self,
        func: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Value[R]:
        return Value(func(self._internal, *args, **kwargs))

    def map_async[**P, R](
        self,
        func: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(func(self._internal, *args, **kwargs))

    def inspect[**P](
        self,
        func: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Value[T]:
        func(self._internal, *args, **kwargs)
        return self

    def inspect_async[**P](
        self,
        func: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[T]:
        @functools.wraps(func)
        async def _inspect_async(
            value: T,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            await func(value, *args, **kwargs)
            return value

        return Future(_inspect_async(self._internal, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](func: Callable[P, R]) -> Callable[P, Value[R]]:
        @functools.wraps(func)
        def _decorator(*args: P.args, **kwargs: P.kwargs) -> Value[R]:
            return Value(func(*args, **kwargs))

        return _decorator
