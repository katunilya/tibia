import pytest

from tibia.pipeline import Pipeline
from tests.curried_example_functions import add, add_async


def test_unwrap():
    assert Pipeline(0).unwrap() == 0


def test_map():
    assert Pipeline(0).map(add(3)).unwrap() == 3


def test_then():
    assert Pipeline(0).then(add(3)) == 3


@pytest.mark.asyncio
async def test_map_async():
    assert await Pipeline(0).map_async(add_async(3)).unwrap() == 3


@pytest.mark.asyncio
async def test_then_async():
    assert await Pipeline(0).then_async(add_async(3)) == 3
