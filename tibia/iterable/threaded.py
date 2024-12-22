from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Concatenate, Iterable


def map[_TValue, **_ParamSpec, _TResult](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Iterable[_TResult]:
    with ThreadPoolExecutor() as _executor:
        for future in as_completed(
            (_executor.submit(func, item, *args, **kwargs) for item in iterable),
        ):
            yield future.result()


def filter[_TValue, **_ParamSpec, _TResult](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], _TResult],
    executor: ThreadPoolExecutor | None = None,
    timeout: float | None = None,
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> Iterable[_TValue]:
    with ThreadPoolExecutor() as _executor:
        future_to_value = {
            _executor.submit(func, item, *args, **kwargs): item for item in iterable
        }
        for future in as_completed(future_to_value, timeout=timeout):
            if future.result():
                yield future_to_value[future]
