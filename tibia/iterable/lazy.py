from typing import Callable, Concatenate, Iterable


def map[T, **P, R](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[R]:
    for item in iterable:
        yield func(item, *args, **kwargs)


def filter[T, **P](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[T]:
    for item in iterable:
        if func(item, *args, **kwargs):
            yield item
