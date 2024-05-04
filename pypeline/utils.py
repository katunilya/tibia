from typing import Callable, Concatenate


def identity[_TValue](value: _TValue) -> _TValue:
    return value  # pragma: no cover


async def async_identity[_TValue](value: _TValue) -> _TValue:
    return value  # pragma: no cover


def curry_first[_TFirst, **_ParamSpec, _TResult](
    func: Callable[Concatenate[_TFirst, _ParamSpec], _TResult],
) -> Callable[_ParamSpec, Callable[[_TFirst], _TResult]]:
    def _curry_first(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
        def __curry_first(first_arg: _TFirst):
            return func(first_arg, *args, **kwargs)

        return __curry_first

    return _curry_first
