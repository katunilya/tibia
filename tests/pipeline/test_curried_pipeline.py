import pytest

from tibia.pipeline import Pipeline


def add(x: int, y: int) -> int:
    return x + y


def subtract(x: int, y: int) -> int:
    return x - y


async def add_async(x: int, y: int) -> int:
    return x + y


def test_pipeline_curring():
    assert Pipeline(3).map(add, 3).map(add, 10).then(subtract, 4) == 3 + 3 + 10 - 4


@pytest.mark.asyncio
async def test_async_pipeline_curring():
    assert (
        await Pipeline(3)
        .map(add, 3)
        .map_async(add_async, 10)
        .map(subtract, 4)
        .map_async(add_async, 2)
        .then(add, 1)
        == 3 + 3 + 10 - 4 + 2 + 1
    )
