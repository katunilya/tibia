from __future__ import annotations

import functools
import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate

from tibia import result as r
from tibia.future import Future


@dataclass(slots=True)
class FutureResult[T, E]:
    _internal: Awaitable[r.Result[T, E]]

    def __await__(self):
        return self._internal.__await__()

    def is_ok(self) -> Future[bool]:
        return Future(is_ok(self))

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_and(self, fn, *args, **kwargs))

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_and_async(self, fn, *args, **kwargs))

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_or(self, fn, *args, **kwargs))

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_or_async(self, fn, *args, **kwargs))

    def expect[T, E](self, what: str) -> Future[T]:
        return Future(expect(self, what))

    def unwrap[T, E](self) -> Future[T]:
        return Future(unwrap(self))

    def unwrap_or(self, default: T) -> Future[T]:
        return Future(unwrap_or(self, default))

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        return FutureResult(map(self, fn, *args, **kwargs))

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[R, E]:
        return FutureResult(map_async(self, fn, *args, **kwargs))

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
        default: T,
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
    ) -> FutureResult[T, E]:
        return FutureResult(inspect(self, fn, *args, **kwargs))

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        return FutureResult(inspect_async(self, fn, *args, **kwargs))

    def is_err(self) -> Future[bool]:
        return Future(is_err(self))

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_and(self, fn, *args, **kwargs))

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_and_async(self, fn, *args, **kwargs))

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_or(self, fn, *args, **kwargs))

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[bool]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_or_async(self, fn, *args, **kwargs))

    def expect_err(self, what: str) -> Future[E]:
        return Future(expect_err(self, what))

    def unwrap_err(self) -> Future[E]:
        return Future(unwrap_err(self))

    def unwrap_err_or(self, default: E) -> Future[E]:
        return Future(unwrap_err_or(self, default))

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        return FutureResult(map_err(self, fn, *args, **kwargs))

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        return FutureResult(map_err_async(self, fn, *args, **kwargs))

    def map_err_or[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(map_err_or(self, default, fn, *args, **kwargs))

    def map_err_or_async[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        return Future(map_err_or_async(self, default, fn, *args, **kwargs))

    def inspect_err[**P](
        self,
        fn: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        return FutureResult(inspect_err(self, fn, *args, **kwargs))

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> FutureResult[T, E]:
        return FutureResult(inspect_err_async(self, fn, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](fn: Callable[P, Awaitable[R]]):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "FutureResult.wraps will be deprecated in tibia@3.0.0, "
            "use future_result.wraps instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(fn)
        def _wraps(*args: P.args, **kwargs: P.kwargs) -> FutureResult[R, Exception]:
            return FutureResult(_async_wraps(fn)(*args, **kwargs))

        return _wraps

    @staticmethod
    def safe(*exceptions: Exception):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "FutureResult.safe will be deprecated in tibia@3.0.0, "
            "use future_result.safe or future_result.safe_from instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        def _safe[**P, R](
            fn: Callable[P, Awaitable[R]],
        ) -> Callable[P, FutureResult[R, Exception]]:
            @functools.wraps(fn)
            def __safe(*args: P.args, **kwargs: P.kwargs) -> FutureResult[R, Exception]:
                return FutureResult(_async_safe(*exceptions)(fn)(*args, **kwargs))

            return __safe

        return _safe


async def is_ok[T, E](fr: FutureResult[T, E]) -> bool:
    return r.is_ok(await fr)


async def is_ok_and[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return r.is_ok_and(await fr, fn, *args, **kwargs)


async def is_ok_and_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await r.is_ok_and_async(await fr, fn, *args, **kwargs)


async def is_ok_or[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return r.is_ok_or(await fr, fn, *args, **kwargs)


async def is_ok_or_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await r.is_ok_or_async(await fr, fn, *args, **kwargs)


async def expect[T, E](fr: FutureResult[T, E], what: str) -> T:
    return r.expect(await fr, what)


async def unwrap[T, E](fr: FutureResult[T, E]) -> T:
    return r.unwrap(await fr)


async def unwrap_or[T, E](fr: FutureResult[T, E], default: T) -> T:
    return r.unwrap_or(await fr, default)


async def map[T, E, **P, R](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[R, E]:
    return r.map(await fr, fn, *args, **kwargs)


async def map_async[T, E, **P, R](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[R, E]:
    return await r.map_async(await fr, fn, *args, **kwargs)


async def map_or[T, E, **P, R](
    fr: FutureResult[T, E],
    default: R,
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return r.map_or(await fr, default, fn, *args, **kwargs)


async def map_or_async[T, E, **P, R](
    fr: FutureResult[T, E],
    default: T,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return await r.map_or_async(await fr, default, fn, *args, **kwargs)


async def inspect[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    return r.inspect(await fr, fn, *args, **kwargs)


async def inspect_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    return await r.inspect_async(await fr, fn, *args, **kwargs)


async def is_err[T, E](fr: FutureResult[T, E]) -> bool:
    return r.is_err(await fr)


async def is_err_and[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return r.is_err_and(await fr, fn, *args, **kwargs)


async def is_err_and_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await r.is_err_and_async(await fr, fn, *args, **kwargs)


async def is_err_or[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return r.is_err_or(await fr, fn, *args, **kwargs)


async def is_err_or_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return await r.is_err_or_async(await fr, fn, *args, **kwargs)


async def expect_err[T, E](fr: FutureResult[T, E], what: str) -> E:
    return r.expect_err(await fr, what)


async def unwrap_err[T, E](fr: FutureResult[T, E]) -> E:
    return r.unwrap_err(await fr)


async def unwrap_err_or[T, E](fr: FutureResult[T, E], default: E) -> E:
    return r.unwrap_err_or(await fr, default)


async def map_err[T, E, **P, R](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, R]:
    return r.map_err(await fr, fn, *args, **kwargs)


async def map_err_async[T, E, **P, R](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, R]:
    return await r.map_err_async(await fr, fn, *args, **kwargs)


async def map_err_or[T, E, **P, R](
    fr: FutureResult[T, E],
    default: R,
    fn: Callable[Concatenate[E, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return r.map_err_or(await fr, default, fn, *args, **kwargs)


async def map_err_or_async[T, E, **P, R](
    fr: FutureResult[T, E],
    default: R,
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return await r.map_err_or_async(await fr, default, fn, *args, **kwargs)


async def inspect_err[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    return r.inspect_err(await fr, fn, *args, **kwargs)


async def inspect_err_async[T, E, **P](
    fr: FutureResult[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> r.Result[T, E]:
    return await r.inspect_err_async(await fr, fn, *args, **kwargs)


def _async_wraps[**P, R](
    fn: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[r.Result[R, Exception]]]:
    @functools.wraps(fn)
    async def _wraps(*args: P.args, **kwargs: P.kwargs) -> r.Result[R, Exception]:
        return r.Ok(await fn(*args, **kwargs))

    return _wraps


def _async_safe(*exceptions: Exception):
    if not exceptions:
        exceptions = (Exception,)

    def _safe[**P, R](
        fn: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[r.Result[R, Exception]]]:
        @functools.wraps(fn)
        async def __safe(*args: P.args, **kwargs: P.kwargs) -> r.Result[R, Exception]:
            try:
                return r.Ok(await fn(*args, **kwargs))
            except exceptions as exc:
                return r.Err(exc)

        return __safe

    return _safe


def wraps[**P, T](
    fn: Callable[P, Awaitable[T]],
) -> Callable[P, FutureResult[T, Exception]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> FutureResult[T, Exception]:
        return FutureResult(_async_wraps(fn)(*args, **kwargs))

    return _wraps


def safe[**P, T](
    fn: Callable[P, Awaitable[T]],
) -> Callable[P, FutureResult[T, Exception]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> FutureResult[T, Exception]:
        return FutureResult(_async_safe()(fn)(*args, **kwargs))

    return _wraps


def safe_from(*exceptions: Exception):
    if not exceptions:
        exceptions = (Exception,)

    def _safe_from[**P, T](
        fn: Callable[P, Awaitable[T]],
    ) -> Callable[P, FutureResult[T, Exception]]:
        @functools.wraps(fn)
        def __safe_from(
            *args: P.args, **kwargs: P.kwargs
        ) -> FutureResult[T, Exception]:
            return FutureResult(_async_safe(*exceptions)(fn)(*args, **kwargs))

        return __safe_from

    return _safe_from
