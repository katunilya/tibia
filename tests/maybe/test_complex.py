import pytest

from tibia.maybe import Empty, Some
from tests.example_functions import add, add_async, multiply, multiply_async, subtract


@pytest.mark.asyncio
async def test_complex_1():
    assert (
        await Some(0)
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


@pytest.mark.asyncio
async def test_complex_2():
    assert (
        await Empty()
        .map(add(100))
        .map(subtract(50))
        .map(multiply(2))
        .map_async(add_async(10))
        .map_async(multiply_async(0))
        .map_async(add_async(20))
        .map(subtract(10))
        .map_async(multiply_async(104))
        .then_or(multiply(0), -1)
    ) == -1


# TODO add more different complex test cases
