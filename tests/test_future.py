import pytest

from tests.utils import add, add_async, set_async
from tibia import mapping
from tibia.future import Future
from tibia.value import Value


@pytest.mark.asyncio
async def test_unwrap():
    result = await Value(1).map_async(add_async, 1).unwrap()
    assert result == 2


@pytest.mark.asyncio
async def test_map():
    result = await Value(0).map_async(add_async, 1).map(add, 1).unwrap()
    assert result == 2


@pytest.mark.asyncio
async def test_map_async():
    result = await Value(0).map_async(add_async, 1).map_async(add_async, 1).unwrap()

    assert result == 2


@pytest.mark.asyncio
async def test_inspect():
    key_1, value_1 = "key_1", "value_1"
    key_2, value_2 = "key_2", "value_2"
    target = {key_1: value_1, key_2: value_2}

    result = (
        await Value({})
        .inspect_async(set_async, key_1, value_1)
        .inspect(mapping.value.set, key_2, value_2)
        .unwrap()
    )

    assert result == target


@pytest.mark.asyncio
async def test_inspect_async():
    key_1, value_1 = "key_1", "value_1"
    key_2, value_2 = "key_2", "value_2"
    target = {key_1: value_1, key_2: value_2}

    result = (
        await Value({})
        .inspect_async(set_async, key_1, value_1)
        .inspect_async(set_async, key_2, value_2)
        .unwrap()
    )

    assert result == target


@pytest.mark.asyncio
async def test_wraps():
    x, y = 1, 1
    wrapped_add_async = Future.wraps(add_async)

    result = wrapped_add_async(x, y)

    assert isinstance(result, Future)
    assert await result.unwrap() == await add_async(x, y)
