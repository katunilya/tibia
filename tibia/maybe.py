from __future__ import annotations

import functools
import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate, cast

from tibia import future_maybe as fm
from tibia.future import Future


class Maybe[T]:
    @staticmethod
    def from_value[I](value: I) -> Maybe[I]:
        return from_value(value)

    @staticmethod
    def from_value_when[I, **P](
        value: I,
        fn: Callable[Concatenate[I, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[I]:
        return from_value_when(value, fn, *args, **kwargs)

    @staticmethod
    def from_optional[I](value: I | None) -> Maybe[I]:
        return from_optional(value)

    @staticmethod
    def from_optional_when[I, **P](
        value: I | None,
        fn: Callable[Concatenate[I, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[I]:
        return from_optional_when(value, fn, *args, **kwargs)

    def is_empty(self) -> bool:
        return is_empty(self)

    def is_empty_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_empty_or(self, fn, *args, **kwargs)

    def is_empty_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_empty_or_async(self, fn, *args, **kwargs))

    def is_some(self) -> bool:
        return is_some(self)

    def is_some_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_some_and(self, fn, *args, **kwargs)

    def is_some_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_some_and_async(self, fn, *args, **kwargs))

    def expect(self, what: str) -> T:
        return expect(self, what)

    def unwrap(self) -> T:
        return unwrap(self)

    def unwrap_or(self, default: T) -> T:
        return unwrap_or(self, default)

    def unwrap_or_none(self) -> T | None:
        return unwrap_or_none(self)

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Maybe[R]:
        return map(self, fn, *args, **kwargs)

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fm.FutureMaybe[R]:
        return fm.FutureMaybe(map_async(self, fn, *args, **kwargs))

    def map_or[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return map_or(self, default, fn, *args, **kwargs)

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
    ) -> Maybe[T]:
        return inspect(self, fn, *args, **kwargs)

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fm.FutureMaybe[T]:
        return fm.FutureMaybe(inspect_async(self, fn, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](fn: Callable[P, R]) -> Callable[P, Maybe[R]]:
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "Maybe.wraps will be deprecated in tibia@3.0.0, use maybe.wraps instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(fn)
        def _wraps(*args: P.args, **kwargs: P.kwargs) -> Maybe[R]:
            return Some(fn(*args, **kwargs))

        return _wraps

    @staticmethod
    def wraps_optional[**P, R](fn: Callable[P, R | None]) -> Callable[P, Maybe[R]]:
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "Maybe.wraps_optional will be deprecated in tibia@3.0.0, "
            "use maybe.safe instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(fn)
        def _wraps_optional(*args: P.args, **kwargs: P.kwargs) -> Maybe[R]:
            return Maybe.from_optional(fn(*args, **kwargs))

        return _wraps_optional


@dataclass(slots=True)
class Some[T](Maybe[T]):
    _internal: T

    def __eq__(self, value: Maybe[Any]):
        if isinstance(value, Some):
            return self._internal.__eq__(value._internal)

        return False


@dataclass(slots=True)
class Empty(Maybe[Any]):
    def __eq__(self, value: Maybe[Any]):
        if value is _Empty or isinstance(value, Empty):
            return True

        return False


_Empty = Empty()


def from_value[T](value: T) -> Maybe[T]:
    return Some(value)


def from_value_when[T, **P](
    value: T,
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    return Some(value) if fn(value, *args, **kwargs) else _Empty


def from_optional[T](value: T | None) -> Maybe[T]:
    return _Empty if value is None else Some(value)


def from_optional_when[T, **P](
    value: T | None,
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    if value is None:
        return _Empty

    if not fn(value, *args, **kwargs):
        return _Empty

    return Some(value)


def is_empty[T](m: Maybe[T]) -> bool:
    return isinstance(m, Empty)


def is_empty_or[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(m, Empty):
        return True

    m = cast(Some, m)
    return fn(m._internal, *args, **kwargs)


async def is_empty_or_async[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(m, Empty):
        return True

    m = cast(Some, m)
    return await fn(m._internal, *args, **kwargs)


def is_some[T](m: Maybe[T]):
    return isinstance(m, Some)


def is_some_and[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(m, Some) and fn(m._internal, *args, **kwargs)


async def is_some_and_async[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(m, Some) and await fn(m._internal, *args, **kwargs)


def expect[T](m: Maybe[T], what: str) -> T:
    if isinstance(m, Some):
        return m._internal

    raise ValueError(what)


def unwrap[T](m: Maybe[T]) -> T:
    return expect(m, "must be some")


def unwrap_or[T](m: Maybe[T], default: T) -> T:
    if isinstance(m, Some):
        return m._internal

    return default


def unwrap_or_none[T](m: Maybe[T]) -> T:
    if isinstance(m, Some):
        return m._internal


def map[T, **P, R](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[R]:
    if isinstance(m, Some):
        return Some(fn(m._internal, *args, **kwargs))

    return _Empty


async def map_async[T, **P, R](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[R]:
    if isinstance(m, Some):
        return Some(await fn(m._internal, *args, **kwargs))

    return _Empty


def map_or[T, **P, R](
    m: Maybe[T],
    default: R,
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(m, Some):
        return fn(m._internal, *args, **kwargs)

    return default


async def map_or_async[T, **P, R](
    m: Maybe[T],
    default: R,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(m, Some):
        return await fn(m._internal, *args, **kwargs)

    return default


def inspect[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    if isinstance(m, Some):
        fn(m._internal, *args, **kwargs)

    return m


async def inspect_async[T, **P](
    m: Maybe[T],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Maybe[T]:
    if isinstance(m, Some):
        await fn(m._internal, *args, **kwargs)

    return m


def match_some[**P, T](*fns: Callable[P, Maybe[T]]) -> Callable[P, Maybe[T]]:
    def _match_some(*args: P.args, **kwargs: P.kwargs) -> Maybe[T]:
        for fn in fns:
            m = fn(*args, **kwargs)

            if m.is_some():
                return m

        return _Empty

    return _match_some


def wraps[**P, T](fn: Callable[P, T]) -> Callable[P, Maybe[T]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> Maybe[T]:
        return Some(fn(*args, **kwargs))

    return _wraps


def safe[**P, T](fn: Callable[P, T | None]) -> Callable[P, Maybe[T]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> Maybe[T]:
        return Maybe.from_optional(fn(*args, **kwargs))

    return _wraps
