import pytest

from tibia.compose import AsyncCompose
from tests.example_functions import add, add_async


@pytest.mark.asyncio
async def test_call():
    _compose = AsyncCompose(add_async(0))
    assert await _compose(10) == 10


@pytest.mark.asyncio
async def test_then():
    _compose = AsyncCompose(add_async(1)).then(add(2)).then(add(3))
    assert await _compose(10) == 10 + 1 + 2 + 3


@pytest.mark.asyncio
async def test_then_async():
    _compose = AsyncCompose(add_async(1)).then(add(2)).then_async(add_async(3))
    assert await _compose(10) == 10 + 1 + 2 + 3
