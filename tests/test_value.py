from inspect import isawaitable

import pytest

from tests.utils import add, add_async, set_async
from tibia import mapping
from tibia.value import Value


def test_unwrap():
    obj = object()

    assert Value(obj).unwrap() is obj


def test_map():
    assert Value(1).map(lambda x: x + 1).unwrap() == 2


def test_inspect():
    key, value = "key", "value"
    target = {key: value}

    assert Value({}).inspect(mapping.value.set, key, value).unwrap() == target


def test_wraps():
    x, y = 1, 1
    wrapped_add = Value.wraps(add)

    result = wrapped_add(x, y)

    assert isinstance(result, Value)
    assert result.unwrap() == add(x, y)


@pytest.mark.asyncio
async def test_map_async():
    result_coroutine = Value(1).map_async(add_async, 1).unwrap()

    assert isawaitable(result_coroutine)

    result = await result_coroutine

    assert result == 1 + 1


@pytest.mark.asyncio
async def test_inspect_async():
    key, value = "key", "value"
    target = {key: value}

    result_coroutine = Value({}).inspect_async(set_async, key, value).unwrap()

    assert isawaitable(result_coroutine)

    result = await result_coroutine

    assert result == target
