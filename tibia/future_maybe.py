from __future__ import annotations

import functools
import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate

from tibia import maybe as m
from tibia.future import Future


@dataclass(slots=True)
class FutureMaybe[T]:
    _internal: Awaitable[m.Maybe[T]]

    def __await__(self):
        return self._internal.__await__()

    @staticmethod
    def from_value[I](value: I) -> FutureMaybe[I]:
        return FutureMaybe(from_value(value))

    @staticmethod
    def from_value_when[I, **P](
        value: I,
        fn: Callable[Concatenate[I, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[I]:
        return FutureMaybe(from_value_when(value, fn, *args, **kwargs))

    @staticmethod
    def from_optional[I](value: I | None) -> FutureMaybe[I]:
        return FutureMaybe(from_optional(value))

    @staticmethod
    def from_optional_when[I, **P](
        value: I | None,
        fn: Callable[Concatenate[I, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[I]:
        return FutureMaybe(from_optional_when(value, fn, *args, **kwargs))

    def is_empty(self) -> Future[bool]:
        return Future(is_empty(self))

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_empty_or(self, fn, *args, **kwargs))

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_empty_or_async(self, fn, *args, **kwargs))

    def is_some(self) -> Future[bool]:
        return Future(is_some(self))

    def is_some_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_some_and(self, fn, *args, **kwargs))

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_some_and_async(self, fn, *args, **kwargs))

    def expect(self, what: str) -> Future[T]:
        return Future(expect(self, what))

    def unwrap(self) -> Future[T]:
        return Future(unwrap(self))

    def unwrap_or(self, default: T) -> Future[T]:
        return Future(unwrap_or(self, default))

    def unwrap_or_none(self) -> Future[T | None]:
        return Future(unwrap_or_none(self))

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe(map(self, fn, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[R]:
        return FutureMaybe(map_async(self, fn, *args, **kwargs))

    def map_or[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(map_or(self, default, fn, *args, **kwargs))

    def map_or_async[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(map_or_async(self, default, fn, *args, **kwargs))

    def inspect[**P](
        self,
        fn: Callable[Concatenate[T, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        return FutureMaybe(inspect(self, fn, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureMaybe[T]:
        return FutureMaybe(inspect_async(self, fn, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](fn: Callable[P, Awaitable[R]]) -> Callable[P, FutureMaybe[R]]:
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "FutureMaybe.wraps will be deprecated in tibia@3.0.0, "
            "use future_maybe.wraps instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(fn)
        def _wraps(*args: P.args, **kwargs: P.kwargs) -> FutureMaybe[R]:
            return FutureMaybe.from_value(fn(*args, **kwargs))

        return _wraps

    @staticmethod
    def wraps_optional[**P, R](
        fn: Callable[P, Awaitable[R | None]],
    ) -> Callable[P, FutureMaybe[R]]:
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "FutureMaybe.wraps_optional will be deprecated in tibia@3.0.0, "
            "use future_maybe.safe instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(fn)
        def _wraps_optional(*args: P.args, **kwargs: P.kwargs) -> FutureMaybe[R]:
            return FutureMaybe.from_optional(fn(*args, **kwargs))

        return _wraps_optional


async def from_value[T](value: Awaitable[T]) -> m.Maybe[T]:
    return m.from_value(await value)


async def from_value_when[T, **P](
    value: Awaitable[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[T]:
    return m.from_value_when(await value, fn, *args, **kwargs)


async def from_optional[T](value: Awaitable[T | None]) -> m.Maybe[T]:
    return m.from_optional(await value)


async def from_optional_when[T, **P](
    value: Awaitable[T | None],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[T]:
    return m.from_optional_when(await value, fn, *args, **kwargs)


async def is_empty[T](fm: FutureMaybe[T]) -> bool:
    return m.is_empty(await fm._internal)


async def is_empty_or[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return m.is_empty_or(await fm._internal, fn, *args, **kwargs)


async def is_empty_or_async[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await m.is_empty_or_async((await fm._internal), fn, *args, **kwargs)


async def is_some[T](fm: FutureMaybe[T]) -> bool:
    return m.is_some(await fm._internal)


async def is_some_and[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return m.is_some_and(await fm._internal, fn, *args, **kwargs)


async def is_some_and_async[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await m.is_some_and_async(await fm._internal, fn, *args, **kwargs)


async def expect[T](fm: FutureMaybe[T], what: str) -> T:
    return m.expect(await fm._internal, what)


async def unwrap[T](fm: FutureMaybe[T]) -> T:
    return m.unwrap(await fm._internal)


async def unwrap_or[T](fm: FutureMaybe[T], default: T) -> T:
    return m.unwrap_or(await fm._internal, default)


async def unwrap_or_none[T](fm: FutureMaybe[T]) -> T | None:
    return m.unwrap_or_none(await fm._internal)


async def map[T, **P, R](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[R]:
    return m.map(await fm._internal, fn, *args, **kwargs)


async def map_async[T, **P, R](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[R]:
    return await m.map_async(await fm._internal, fn, *args, **kwargs)


async def map_or[T, **P, R](
    fm: FutureMaybe[T],
    default: R,
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
):
    return m.map_or(await fm._internal, default, fn, *args, **kwargs)


async def map_or_async[T, **P, R](
    fm: FutureMaybe[T],
    default: R,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return await m.map_or_async(await fm._internal, default, fn, *args, **kwargs)


async def inspect[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[T]:
    return m.inspect(await fm._internal, fn, *args, **kwargs)


async def inspect_async[T, **P](
    fm: FutureMaybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> m.Maybe[T]:
    return await m.inspect_async(await fm._internal, fn, *args, **kwargs)


def wraps[**P, T](fn: Callable[P, Awaitable[T]]) -> Callable[P, FutureMaybe[T]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> FutureMaybe[T]:
        return FutureMaybe.from_value(fn(*args, **kwargs))

    return _wraps


def safe[**P, T](
    fn: Callable[P, Awaitable[T | None]],
) -> Callable[P, FutureMaybe[T]]:
    @functools.wraps(fn)
    def _safe(*args: P.args, **kwargs: P.kwargs) -> FutureMaybe[T]:
        return FutureMaybe.from_optional(fn(*args, **kwargs))

    return _safe
