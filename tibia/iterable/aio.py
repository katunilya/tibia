import asyncio
from typing import Awaitable, Callable, Concatenate, Iterable


async def map[T, **P, R](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> list[R]:
    return await asyncio.gather(*[func(item, *args, **kwargs) for item in iterable])


async def filter[T, **P](
    iterable: Iterable[T],
    func: Callable[Concatenate[T, P], Awaitable[bool]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> list[T]:
    async def _func(item: T, *args: P.args, **kwargs: P.kwargs) -> tuple[bool, T]:
        return (await func(item, *args, **kwargs), item)

    tasks = [asyncio.create_task(_func(item, *args, **kwargs)) for item in iterable]
    result = []

    for task in asyncio.as_completed(tasks):
        predicate, item = await task

        if predicate:
            result.append(item)

    return result
