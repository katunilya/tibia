from typing import Any, Callable, Concatenate, Iterable, Mapping

from tibia.maybe import Maybe


def map[K, V, **P, R](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[V, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[K, R]:
    return {key: func(value, *args, **kwargs) for key, value in mapping.items()}


def filter[K, V, **P](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[V, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[K, V]:
    return {
        key: value for key, value in mapping.items() if func(value, *args, **kwargs)
    }


def iterate[V](mapping: Mapping[Any, V]) -> Iterable[V]:
    yield from mapping.values()


def set[K, V](mapping: Mapping[K, V], key: K, value: V) -> None:
    mapping[key] = value


def get[K, V](mapping: Mapping[K, V], key: K) -> V:
    return mapping[key]


def get_or[K, V](mapping: Mapping[K, V], key: K, default: V) -> V:
    return mapping.get(key, default)


def maybe_get[K, V](mapping: Mapping[K, V], key: K) -> Maybe[V]:
    return Maybe.from_optional(mapping.get(key, None))
