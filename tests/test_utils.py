import pytest

from tibia.utils import async_identity, identity, passing


def test_identity():
    assert identity(3) == 3


@pytest.mark.asyncio
async def test_async_identity():
    assert await async_identity(3) == 3


def test_passing():
    def returns_none(value: int): ...

    assert passing(returns_none)(0) == 0
