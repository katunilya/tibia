from __future__ import annotations

from functools import reduce as _py_reduce
from typing import Any, Callable, Concatenate, Iterable, Mapping

from tibia.utils import identity


def map[T, **P, R](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> list[R]:
    return [func(item, *args, **kwargs) for item in iterable]


def filter[T, **P](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> list[T]:
    return [item for item in iterable if func(item, *args, **kwargs)]


def reduce[T, **P](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, T, P], T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    return _py_reduce(
        lambda acc, nxt: func(acc, nxt, *args, **kwargs),
        iterable,
    )


def reduce_to[T, R, **P](
    iterable: Iterable[T],
    func: Callable[Concatenate[R, T, P], R],
    initial: R,
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return _py_reduce(
        lambda acc, nxt: func(acc, nxt, *args, **kwargs),
        iterable,
        initial,
    )


def sort_asc[T, **P](
    iterable: Iterable[T],
    key: Callable[Concatenate[T, P], Any] | None = None,
    *args,
    **kwargs,
) -> list[T]:
    if not key:
        key, args, kwargs = identity, (), {}

    return sorted(iterable, key=lambda v: key(v, *args, **kwargs))


def sort_desc[T, **P](
    iterable: Iterable[T],
    key: Callable[Concatenate[T, P], Any] | None = None,
    *args: P.args,
    **kwargs: P.kwargs,
) -> list[T]:
    if not key:
        key, args, kwargs = identity, (), {}

    return sorted(iterable, key=lambda v: key(v, *args, **kwargs), reverse=True)


def take[T](
    iterable: Iterable[T],
    count: int,
) -> list[T]:
    if count == 0:
        return []
    elif count > 0:
        return [item for i, item in enumerate(iterable) if i < count]
    else:
        _iterable = list(iterable)
        _iterable_len = len(_iterable)
        return [item for i, item in enumerate(_iterable) if i >= _iterable_len + count]


def first[T](
    iterable: Iterable[T],
    default: T | None = None,
) -> T | None:
    for item in iterable:
        return item

    return default


def skip[T](
    iterable: Iterable[T],
    count: int,
) -> Iterable[T]:
    if count == 0:
        return list(iterable)
    elif count > 0:
        return [item for i, item in enumerate(iterable) if i >= count]
    else:
        _iterable = list(iterable)
        _iterable_len = len(_iterable)
        return [item for i, item in enumerate(_iterable) if i < _iterable_len + count]


def join[T](iterables: Iterable[Iterable[T]]) -> list[T]:
    return [item for iterable in iterables for item in iterable]


def group_by[T, **P, K](
    iterable: Iterable[T],
    fn: Callable[Concatenate[T, P], K],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[K, list[T]]:
    mapping = dict[K, list[T]]()

    for item in iterable:
        key = fn(item, *args, **kwargs)

        if key not in mapping:
            mapping[key] = []

        mapping[key].append(item)

    return mapping
