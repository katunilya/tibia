from __future__ import annotations

from typing import Callable, Concatenate


def all_[T](*pfns: Callable[[T], bool]) -> Callable[[T], bool]:
    return lambda t: all(fn(t) for fn in pfns)


def any_[T](*pfns: Callable[[T], bool]) -> Callable[[T], bool]:
    return lambda t: any(fn(t) for fn in pfns)


def not_[T, **P](
    pfn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Callable[[T], bool]:
    return lambda t: not pfn(t, *args, **kwargs)


class where[T, **P]:
    pfn: Callable[[T], bool]

    def __init__(
        self,
        pfn: Callable[Concatenate[T, P], bool],
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        self.pfn = lambda t: pfn(t, *args, **kwargs)

    def __call__(self, value: T) -> bool:
        return self.pfn(value)

    def or_[**P_](
        self,
        pfn: Callable[Concatenate[T, P_], bool],
        *args: P_.args,
        **kwargs: P_.kwargs,
    ) -> where[T]:
        return where(lambda t: self.pfn(t) or pfn(t, *args, **kwargs))

    def and_[**P_](
        self,
        pfn: Callable[Concatenate[T, P_], bool],
        *args: P_.args,
        **kwargs: P_.kwargs,
    ) -> where[T]:
        return where(lambda t: self.pfn(t) and pfn(t, *args, **kwargs))

    def unwrap(self) -> Callable[[T], bool]:
        return self


def when[T, **P](
    value: T,
    pfn: Callable[[T], bool],
    fn: Callable[Concatenate[T, P], T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    return fn(value, *args, **kwargs) if pfn(value) else value


def when_or[T, **P, R](
    value: T,
    pfn: Callable[[T], bool],
    other: R,
    fn: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return fn(value, *args, **kwargs) if pfn(value) else other
