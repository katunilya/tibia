from inspect import isawaitable

import pytest

from tests.conftest import add, add_async, multiply, subtract, subtract_async
from tibia.pipeline import Pipeline


def test_pipeline():
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
