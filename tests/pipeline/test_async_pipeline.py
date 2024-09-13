import pytest

from tibia.pipeline import AsyncPipeline
from tibia.utils import async_identity
from tests.curried_example_functions import add, add_async


@pytest.mark.asyncio
async def test_unwrap():
    assert await AsyncPipeline(async_identity(0)).unwrap() == 0


@pytest.mark.asyncio
async def test_map():
    assert await AsyncPipeline(async_identity(0)).map(add(3)).unwrap() == 3


@pytest.mark.asyncio
async def test_then():
    assert await AsyncPipeline(async_identity(0)).then(add(3)) == 3


@pytest.mark.asyncio
async def test_map_async():
    assert await AsyncPipeline(async_identity(0)).map_async(add_async(3)).unwrap() == 3


@pytest.mark.asyncio
async def test_then_async():
    assert await AsyncPipeline(async_identity(0)).then_async(add_async(3)) == 3
