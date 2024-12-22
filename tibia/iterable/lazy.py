from typing import Callable, Concatenate, Iterable


def map[_TValue, **_ParamSpec, _TResult](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Iterable[_TResult]:
    for item in iterable:
        yield func(item, *args, **kwargs)


def filter[_TValue, **_ParamSpec](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], bool],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Iterable[_TValue]:
    for item in iterable:
        if func(item, *args, **kwargs):
            yield item
