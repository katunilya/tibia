from typing import Callable, Concatenate


def curried[_TFirst, **_ParamSpec, _TResult](
    func: Callable[Concatenate[_TFirst, _ParamSpec], _TResult],
) -> Callable[_ParamSpec, Callable[[_TFirst], _TResult]]:
    def _curried(*args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs):
        def __curried(first_arg: _TFirst):
            return func(first_arg, *args, **kwargs)

        return __curried

    return _curried
