import pytest

from tibia.pipeline import Pipeline
from tests.example_functions import add, add_async, multiply, multiply_async, subtract


@pytest.mark.asyncio
async def test_complex_1():
    assert (
        await Pipeline(0)
        .map(add(100))
        .map(subtract(50))
        .map(multiply(2))
        .map_async(add_async(10))
        .map_async(multiply_async(0))
        .map_async(add_async(20))
        .map(subtract(10))
        .map_async(multiply_async(104))
        .then(multiply(0))
    ) == 0


# TODO add more different complex test cases
