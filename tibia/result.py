from __future__ import annotations

import functools
import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate, cast

from tibia import future_result as fr
from tibia.future import Future


class Result[T, E]:
    def is_ok(self) -> bool:
        return is_ok(self)

    def is_ok_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_ok_and(self, fn, *args, **kwargs)

    def is_ok_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_and_async(self, fn, *args, **kwargs))

    def is_ok_or[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_ok_or(self, fn, *args, **kwargs)

    def is_ok_or_async[**P](
        self,
        fn: Callable[Concatenate[E, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_ok_or_async(self, fn, *args, **kwargs))

    def expect(self, what: str) -> T:
        return expect(self, what)

    def unwrap(self) -> T:
        return unwrap(self)

    def unwrap_or(self, default: T) -> T:
        return unwrap_or(self, default)

    def map[**P, R](
        self,
        fn: Callable[Concatenate[T, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[R, E]:
        return map(self, fn, *args, **kwargs)

    def map_async[**P, R](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fr.FutureResult[R, E]:
        return fr.FutureResult(map_async(self, fn, *args, **kwargs))

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
    ) -> Result[T, E]:
        return inspect(self, fn, *args, **kwargs)

    def inspect_async[**P](
        self,
        fn: Callable[Concatenate[T, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fr.FutureResult[T, E]:
        return fr.FutureResult(inspect_async(self, fn, *args, **kwargs))

    def is_err(self) -> bool:
        return is_err(self)

    def is_err_and[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_err_and(self, fn, *args, **kwargs)

    def is_err_and_async[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_and_async(self, fn, *args, **kwargs))

    def is_err_or[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> bool:
        return is_err_or(self, fn, *args, **kwargs)

    def is_err_or_async[**P](
        self,
        fn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[bool]:
        return Future(is_err_or_async(self, fn, *args, **kwargs))

    def expect_err(self, what: str) -> E:
        return expect_err(self, what)

    def unwrap_err(self) -> E:
        return unwrap_err(self)

    def unwrap_err_or(self, default: E) -> E:
        return unwrap_err_or(self, default)

    def map_err[**P, R](
        self,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, R]:
        return map_err(self, fn, *args, **kwargs)

    def map_err_async[**P, R](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fr.FutureResult[T, R]:
        return fr.FutureResult(map_err_async(self, fn, *args, **kwargs))

    def map_err_or[**P, R](
        self,
        default: R,
        fn: Callable[Concatenate[E, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return map_err_or(self, default, fn, *args, **kwargs)

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
    ) -> Result[T, E]:
        return inspect_err(self, fn, *args, **kwargs)

    def inspect_err_async[**P](
        self,
        fn: Callable[Concatenate[E, P], Awaitable[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> fr.FutureResult[T, E]:
        return fr.FutureResult(inspect_err_async(self, fn, *args, **kwargs))

    @staticmethod
    def wraps[**P, R](func: Callable[P, R]) -> Callable[P, Result[R, Exception]]:
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "Result.wraps will be deprecated in tibia@3.0.0, "
            "use result.wraps instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        @functools.wraps(func)
        def _wraps(*args: P.args, **kwargs: P.kwargs) -> Result[R, Exception]:
            return Ok(func(*args, **kwargs))

        return _wraps

    @staticmethod
    def safe(*exceptions: Exception):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "Result.safe will be deprecated in tibia@3.0.0, "
            "use result.safe or result.safe_from instead",
            DeprecationWarning,
        )
        warnings.simplefilter("default", DeprecationWarning)

        if not exceptions:
            exceptions = (Exception,)

        def _safe[**P, R](func: Callable[P, R]) -> Callable[P, Result[R, Exception]]:
            @functools.wraps(func)
            def __safe(*args: P.args, **kwargs: P.kwargs) -> Result[R, Exception]:
                try:
                    return Ok(func(*args, **kwargs))
                except exceptions as exc:
                    return Err(exc)

            return __safe

        return _safe


@dataclass(slots=True)
class Ok[T](Result[T, Any]):
    _internal: T

    def __eq__(self, result: Result):
        if not isinstance(result, Ok):
            return self._internal.__eq__(result)

        return self._internal.__eq__(result._internal)


@dataclass(slots=True)
class Err[E](Result[Any, E]):
    _internal: E

    def __eq__(self, result: Result):
        if not isinstance(result, Err):
            return self._internal.__eq__(result)

        return self._internal.__eq__(result._internal)


def is_ok[T, E](r: Result[T, E]) -> bool:
    return isinstance(r, Ok)


def is_ok_and[T, E, **P](
    result: Result[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(result, Ok) and fn(result._internal, *args, **kwargs)


async def is_ok_and_async[T, E, **P](
    result: Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(result, Ok) and await fn(result._internal, *args, **kwargs)


def is_ok_or[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(r, Ok):
        return True

    r = cast(Err, r)
    return fn(r._internal, *args, **kwargs)


async def is_ok_or_async[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(r, Ok):
        return True

    r = cast(Err, r)
    return await fn(r._internal, *args, **kwargs)


def expect[T, E](r: Result[T, E], what: str) -> T:
    if isinstance(r, Ok):
        return r._internal

    raise ValueError(what)


def unwrap[T, E](r: Result[T, E]) -> T:
    return expect(r, "must be ok")


def unwrap_or[T, E](r: Result[T, E], default: T) -> T:
    if isinstance(r, Ok):
        return r._internal

    return default


def map[T, E, **P, R](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[R, E]:
    if isinstance(r, Ok):
        return Ok(fn(r._internal, *args, **kwargs))

    return r


async def map_async[T, E, **P, R](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[R, E]:
    if isinstance(r, Ok):
        return Ok(await fn(r._internal, *args, **kwargs))

    return r


def map_or[T, E, **P, R](
    r: Result[T, E],
    default: R,
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(r, Ok):
        return fn(r._internal, *args, **kwargs)

    return default


async def map_or_async[T, E, **P, R](
    r: Result[T, E],
    default: T,
    fn: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(r, Ok):
        return await fn(r._internal, *args, **kwargs)

    return default


def inspect[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, E]:
    if isinstance(r, Ok):
        fn(r._internal, *args, **kwargs)

    return r


async def inspect_async[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, E]:
    if isinstance(r, Ok):
        await fn(r._internal, *args, **kwargs)

    return r


def is_err[T, E](r: Result[T, E]) -> bool:
    return isinstance(r, Err)


def is_err_and[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(r, Err) and fn(r._internal, *args, **kwargs)


async def is_err_and_async[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    return isinstance(r, Err) and await fn(r._internal, *args, **kwargs)


def is_err_or[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(r, Err):
        return True

    r = cast(Ok, r)
    return fn(r._internal, *args, **kwargs)


async def is_err_or_async[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    if isinstance(r, Err):
        return True

    r = cast(Ok, r)
    return await fn(r._internal, *args, **kwargs)


def expect_err[T, E](r: Result[T, E], what: str) -> E:
    if isinstance(r, Err):
        return r._internal

    raise ValueError(what)


def unwrap_err[T, E](r: Result[T, E]) -> E:
    return expect_err(r, "must be err")


def unwrap_err_or[T, E](r: Result[T, E], default: E) -> E:
    if isinstance(r, Err):
        return r._internal

    return default


def map_err[T, E, **P, R](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, R]:
    if isinstance(r, Err):
        return Err(fn(r._internal, *args, **kwargs))

    return r


async def map_err_async[T, E, **P, R](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, R]:
    if isinstance(r, Err):
        return Err(await fn(r._internal, *args, **kwargs))

    return r


def map_err_or[T, E, **P, R](
    r: Result[T, E],
    default: R,
    fn: Callable[Concatenate[E, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(r, Err):
        return fn(r._internal, *args, **kwargs)

    return default


async def map_err_or_async[T, E, **P, R](
    r: Result[T, E],
    default: R,
    fn: Callable[Concatenate[E, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    if isinstance(r, Err):
        return await fn(r._internal, *args, **kwargs)

    return default


def inspect_err[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, E]:
    if isinstance(r, Err):
        fn(r._internal, *args, **kwargs)

    return r


async def inspect_err_async[T, E, **P](
    r: Result[T, E],
    fn: Callable[Concatenate[E, P], Awaitable[Any]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, E]:
    if isinstance(r, Err):
        await fn(r._internal, *args, **kwargs)

    return r


def match_ok[**P, T, E](*fns: Callable[P, Result[T, E]]) -> Callable[P, Result[T, E]]:
    def _match_ok(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        for fn in fns:
            r = fn(*args, **kwargs)

            if r.is_ok():
                return r

        return Err(ValueError("no option returned ok"))

    return _match_ok


def wraps[**P, T](fn: Callable[P, T]) -> Callable[P, Result[T, Exception]]:
    @functools.wraps(fn)
    def _wraps(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
        return Ok(fn(*args, **kwargs))

    return _wraps


def safe_from(*exceptions: Exception):
    if not exceptions:
        exceptions = (Exception,)

    def _safe_from[**P, T](fn: Callable[P, T]) -> Callable[P, Result[T, Exception]]:
        @functools.wraps(fn)
        def __safe_from(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
            try:
                return Ok(fn(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return __safe_from

    return _safe_from


def safe[**P, T](fn: Callable[P, T]) -> Callable[P, Result[T, Exception]]:
    @functools.wraps(fn)
    def _safe(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
        try:
            return Ok(fn(*args, **kwargs))
        except Exception as exc:
            return Err(exc)

    return _safe
