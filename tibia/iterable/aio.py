import asyncio
from typing import Awaitable, Callable, Concatenate, Iterable


async def map[_TValue, **_ParamSpec, _TResult](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[_TResult]],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> list[_TResult]:
    return await asyncio.gather(*[func(item, *args, **kwargs) for item in iterable])


async def filter[_TValue, **_ParamSpec](
    iterable: Iterable[_TValue],
    func: Callable[Concatenate[_TValue, _ParamSpec], Awaitable[bool]],
    *args: _ParamSpec.args,
    **kwargs: _ParamSpec.kwargs,
) -> list[_TValue]:
    async def _func(
        item: _TValue, *args: _ParamSpec.args, **kwargs: _ParamSpec.kwargs
    ) -> tuple[bool, _TValue]:
        return (await func(item, *args, **kwargs), item)

    tasks = [asyncio.create_task(_func(item, *args, **kwargs)) for item in iterable]
    result = []

    for task in asyncio.as_completed(tasks):
        predicate, item = await task

        if predicate:
            result.append(item)

    return result
