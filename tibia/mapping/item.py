from typing import Callable, Concatenate, Iterable, Mapping


def map[K, V, _K, _V, **P](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[K, V, P], tuple[_K, _V]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[_K, _V]:
    result = {}

    for _key, _value in mapping.items():
        _n_key, _n_value = func(_key, _value, *args, **kwargs)
        result[_n_key] = _n_value

    return result


def map_to_value[K, V, _V, **P](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[K, V, P], _V],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[K, _V]:
    return {key: func(key, value, *args, **kwargs) for key, value in mapping.items()}


def map_to_key[K, V, _K, **P](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[K, V, P], _K],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[_K, V]:
    return {func(key, value, *args, **kwargs): value for key, value in mapping.items()}


def filter[K, V, **P](
    mapping: Mapping[K, V],
    func: Callable[Concatenate[K, V, P], bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Mapping[K, V]:
    return {
        key: value
        for key, value in mapping.items()
        if func(key, value, *args, **kwargs)
    }


def iterate[K, V](
    mapping: Mapping[K, V],
) -> Iterable[tuple[K, V]]:
    for key, value in mapping.items():
        yield (key, value)
