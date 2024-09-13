import pytest

from tibia.maybe import AsyncMaybe, Empty, Some, maybe_returns_async
from tibia.pipeline import AsyncPipeline
from tibia.result import AsyncResult
from tests.curried_example_functions import add, add_async, can_return_optional_async


async def some_int_async(value: int):
    return Some(value).as_maybe()


async def empty_int_async():
    return Empty().as_maybe(int)


@pytest.mark.asyncio
async def test_unwrap():
    assert await AsyncMaybe(some_int_async(0)).unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).unwrap()


@pytest.mark.asyncio
async def test_unwrap_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncMaybe(some_int_async(0)).unwrap_or(other) == 0
    assert await AsyncMaybe(some_int_async(0)).unwrap_or(other_func) == 0
    assert await AsyncMaybe(empty_int_async()).unwrap_or(other) == other
    assert await AsyncMaybe(empty_int_async()).unwrap_or(other_func) == other_func()


@pytest.mark.asyncio
async def test_unwrap_as_optional():
    assert await AsyncMaybe(some_int_async(0)).unwrap_as_optional() == 0
    assert await AsyncMaybe(empty_int_async()).unwrap_as_optional() is None


@pytest.mark.asyncio
async def test_unwrap_as_pipeline():
    pipeline = AsyncMaybe(some_int_async(0)).unwrap_as_pipeline()

    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).unwrap_as_pipeline().unwrap()


@pytest.mark.asyncio
async def test_unwrap_as_pipeline_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    pipeline = AsyncMaybe(some_int_async(0)).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    pipeline = AsyncMaybe(some_int_async(0)).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    pipeline = AsyncMaybe(empty_int_async()).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == other

    pipeline = AsyncMaybe(empty_int_async()).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == other_func()


@pytest.mark.asyncio
async def test_unwrap_as_result():
    result = AsyncMaybe(some_int_async(0)).unwrap_as_result()

    assert isinstance(result, AsyncResult)
    assert await result.unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).unwrap_as_result().unwrap()


@pytest.mark.asyncio
async def test_unwrap_as_result_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    result = AsyncMaybe(some_int_async(0)).unwrap_as_result_or(other)
    assert isinstance(result, AsyncResult)
    assert await result.unwrap() == 0

    result = AsyncMaybe(some_int_async(0)).unwrap_as_result_or(other_func)
    assert isinstance(result, AsyncResult)
    assert await result.unwrap() == 0

    result = AsyncMaybe(empty_int_async()).unwrap_as_result_or(other)
    assert isinstance(result, AsyncResult)
    assert await result.unwrap() == other

    result = AsyncMaybe(empty_int_async()).unwrap_as_result_or(other_func)
    assert isinstance(result, AsyncResult)
    assert await result.unwrap() == other_func()


@pytest.mark.asyncio
async def test_map():
    assert await AsyncMaybe(some_int_async(0)).map(add(1)).unwrap() == 1

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).map(add(1)).unwrap()


@pytest.mark.asyncio
async def test_then():
    assert await AsyncMaybe(some_int_async(0)).then(add(1)) == 1

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).then(add(1))


@pytest.mark.asyncio
async def test_then_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncMaybe(some_int_async(0)).then_or(add(10), other) == 10
    assert await AsyncMaybe(some_int_async(0)).then_or(add(10), other_func) == 10
    assert await AsyncMaybe(empty_int_async()).then_or(add(10), other) == other
    assert (
        await AsyncMaybe(empty_int_async()).then_or(add(10), other_func) == other_func()
    )


@pytest.mark.asyncio
async def test_map_async():
    assert await AsyncMaybe(some_int_async(0)).map_async(add_async(1)).unwrap() == 1

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).map_async(add_async(1)).unwrap()


@pytest.mark.asyncio
async def test_then_async():
    assert await AsyncMaybe(some_int_async(0)).then_async(add_async(1)) == 1

    with pytest.raises(ValueError):
        await AsyncMaybe(empty_int_async()).then_async(add_async(1))


@pytest.mark.asyncio
async def test_then_or_async():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncMaybe(some_int_async(0)).then_or_async(add_async(10), other) == 10
    assert (
        await AsyncMaybe(some_int_async(0)).then_or_async(add_async(10), other_func)
        == 10
    )
    assert (
        await AsyncMaybe(empty_int_async()).then_or_async(add_async(10), other) == other
    )
    assert (
        await AsyncMaybe(empty_int_async()).then_or_async(add_async(10), other_func)
        == other_func()
    )


@pytest.mark.asyncio
async def test_maybe_returns_async():
    return_empty = maybe_returns_async(can_return_optional_async)
    async_maybe = return_empty(True)

    assert isinstance(async_maybe, AsyncMaybe)

    assert await async_maybe.unwrap_as_optional() is None
    assert await return_empty(False).unwrap_as_optional() is not None
