from typing import Any, Callable, Concatenate, Iterable, Mapping

from tibia.maybe import Maybe


def map[_TKey, _TValue, **_ParamSpec, _TResult](
    mapping: Mapping[_TKey, _TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Mapping[_TKey, _TResult]:
    return {key: func(value, *args, **kwargs) for key, value in mapping.items()}


def filter[_TKey, _TValue, **_ParamSpec](
    mapping: Mapping[_TKey, _TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], bool],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Mapping[_TKey, _TValue]:
    return {
        key: value for key, value in mapping.items() if func(value, *args, **kwargs)
    }


def iterate[_TValue](mapping: Mapping[Any, _TValue]) -> Iterable[_TValue]:
    yield from mapping.values()


def set[K, V](mapping: Mapping[K, V], key: K, value: V) -> None:
    mapping[key] = value


def get[K, V](mapping: Mapping[K, V], key: K) -> V:
    return mapping[key]


def get_or[K, V](mapping: Mapping[K, V], key: K, default: V) -> V:
    return mapping.get(key, default)


def maybe_get[K, V](mapping: Mapping[K, V], key: K) -> Maybe[V]:
    return Maybe.from_optional(mapping.get(key, None))
