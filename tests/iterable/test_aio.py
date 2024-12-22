import pytest

from tests.utils import add, add_async, is_even, is_even_async
from tibia import iterable


@pytest.mark.asyncio
async def test_map(numbers: list[int]):
    result = await iterable.aio.map(numbers, add_async, 1)

    assert result == [add(x, 1) for x in numbers]


@pytest.mark.asyncio
async def test_filter(numbers: list[int]):
    result = await iterable.aio.filter(numbers, is_even_async)

    assert result == [x for x in numbers if is_even(x)]
