import pytest

from tibia.compose import Compose
from tests.example_functions import add, add_async


def test_call():
    _compose = Compose(add(0))
    assert _compose(10) == 10


def test_then():
    _compose = Compose(add(1)).then(add(2)).then(add(3))
    assert _compose(10) == 10 + 1 + 2 + 3


@pytest.mark.asyncio
async def test_then_async():
    _compose = Compose(add(1)).then(add(2)).then_async(add_async(3))
    assert await _compose(10) == 10 + 1 + 2 + 3
