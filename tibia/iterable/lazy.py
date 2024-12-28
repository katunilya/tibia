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


def skip_while[T, **P](
    iterable: Iterable[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[T]:
    is_skipping = True

    for item in iterable:
        is_skipping = fn(item, *args, **kwargs) if is_skipping else False

        if is_skipping:
            continue

        yield item


def take_while[T, **P](
    iterable: Iterable[T],
    fn: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[T]:
    for item in iterable:
        if fn(item, *args, **kwargs):
            yield item
            continue

        break


def join[T](iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    for sub_iterable in iterable:
        yield from sub_iterable
