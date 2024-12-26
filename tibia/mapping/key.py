from typing import Any, Callable, Concatenate, Iterable, Mapping


def map[T, V, **P, R](
    mapping: Mapping[T, V],
    func: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[R, V]:
    return {func(key, *args, **kwargs): value for key, value in mapping.items()}


def filter[T, V, **P](
    mapping: Mapping[T, V],
    func: Callable[Concatenate[T, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[T, V]:
    return {key: value for key, value in mapping.items() if func(key, *args, **kwargs)}


def iterate[T](mapping: Mapping[T, Any]) -> Iterable[T]:
    yield from mapping.keys()
