from inspect import isawaitable

import pytest

from tests.conftest import add, add_async, multiply, subtract, subtract_async
from tibia.pipeline import Pipeline


def test_pipeline_map_unwrap():
    result = (
        Pipeline(0)
        .map(add, 1)
        .map(add, 1)
        .map(multiply, 10)
        .map(subtract, 3)
        .map(add, 7)
        .unwrap()
    )

    assert result == ((0 + 1 + 1) * 10 - 3 + 7)


def test_pipeline_map_apply():
    result = (
        Pipeline(0)
        .map(add, 1)
        .map(add, 1)
        .map(multiply, 10)
        .map(subtract, 3)
        .apply(add, 7)
    )

    assert result == ((0 + 1 + 1) * 10 - 3 + 7)


@pytest.mark.asyncio
async def test_async_pipeline_map_unwrap():
    awaitable_result = (
        Pipeline(0)
        .map(add, 1)
        .map_async(add_async, 1)
        .map(multiply, 10)
        .map_async(subtract_async, 3)
        .map(add, 7)
        .unwrap()
    )
    assert isawaitable(awaitable_result)

    result = await awaitable_result

    assert result == ((0 + 1 + 1) * 10 - 3 + 7)


@pytest.mark.asyncio
async def test_async_pipeline_map_apply():
    awaitable_result = (
        Pipeline(0)
        .map(add, 1)
        .map_async(add_async, 1)
        .map(multiply, 10)
        .map_async(subtract_async, 3)
        .apply(add, 7)
    )

    assert isawaitable(awaitable_result)

    result = await awaitable_result

    assert result == ((0 + 1 + 1) * 10 - 3 + 7)


@pytest.mark.asyncio
async def test_async_pipeline_map_apply_async():
    awaitable_result = (
        Pipeline(0)
        .map(add, 1)
        .map_async(add_async, 1)
        .map(multiply, 10)
        .map_async(subtract_async, 3)
        .apply_async(add_async, 7)
    )

    assert isawaitable(awaitable_result)

    result = await awaitable_result

    assert result == ((0 + 1 + 1) * 10 - 3 + 7)


@pytest.mark.asyncio
async def test_pipeline_apply_async():
    awaitable_result = Pipeline(0).apply_async(add_async, 10)

    assert isawaitable(awaitable_result)

    result = await awaitable_result

    assert result == 10
