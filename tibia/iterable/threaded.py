from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Concatenate, Iterable


def map[T, **P, R](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[R]:
    with ThreadPoolExecutor() as _executor:
        for future in as_completed(
            (_executor.submit(func, item, *args, **kwargs) for item in iterable),
        ):
            yield future.result()


def filter[T, **P, R](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> Iterable[T]:
    with ThreadPoolExecutor() as _executor:
        future_to_value = {
            _executor.submit(func, item, *args, **kwargs): item for item in iterable
        }
        for future in as_completed(future_to_value):
            if future.result():
                yield future_to_value[future]
