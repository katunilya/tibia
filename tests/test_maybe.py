from typing import Any, Awaitable, Callable

import pytest

from tests.utils import add, add_async, is_even, is_even_async, set_async
from tibia import mapping
from tibia.maybe import Empty, Maybe, Some


@pytest.mark.parametrize(
    "value",
    [
        1,
        None,
    ],
)
def test_form_value(value: Any):
    assert Maybe.from_value(value) == Some(value)


@pytest.mark.parametrize(
    ("value", "fn", "target"),
    [
        (1, is_even, Empty()),
        (0, is_even, Some(0)),
    ],
)
def test_from_value_when(value: int, fn: Callable[[int], bool], target: Maybe[int]):
    assert Maybe.from_value_when(value, fn) == target


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (1, Some(1)),
        (None, Empty()),
    ],
)
def test_from_optional(value: int | None, target: Maybe[int]):
    assert Maybe.from_optional(value) == target


@pytest.mark.parametrize(
    ("value", "fn", "target"),
    [
        (None, is_even, Empty()),
        (0, is_even, Some(0)),
        (1, is_even, Empty()),
    ],
)
def test_from_optional_when(
    value: int | None,
    fn: Callable[[int], bool],
    target: Maybe[int],
):
    assert Maybe.from_optional_when(value, fn) == target


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(1), False),
        (Empty(), True),
    ],
)
def test_is_empty(maybe: Maybe[int], target: bool):
    assert maybe.is_empty() == target


@pytest.mark.parametrize(
    ("maybe", "fn", "target"),
    [
        (Some(1), is_even, False),
        (Some(2), is_even, True),
        (Empty(), is_even, True),
    ],
)
def test_is_empty_or(maybe: Maybe[int], fn: Callable[[int], bool], target: bool):
    assert maybe.is_empty_or(fn) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("maybe", "fn", "target"),
    [
        (Some(1), is_even_async, False),
        (Some(2), is_even_async, True),
        (Empty(), is_even_async, True),
    ],
)
async def test_is_empty_or_async(
    maybe: Maybe[int],
    fn: Callable[[int], Awaitable[bool]],
    target: bool,
):
    assert (await maybe.is_empty_or_async(fn)) == target


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(1), True),
        (Empty(), False),
    ],
)
def test_is_some(maybe: Maybe[int], target: bool):
    assert maybe.is_some() is target


@pytest.mark.parametrize(
    ("maybe", "fn", "target"),
    [
        (Some(2), is_even, True),
        (Some(1), is_even, False),
        (Empty(), is_even, False),
    ],
)
def test_is_some_and(maybe: Maybe[int], fn: Callable[[int], bool], target: bool):
    assert maybe.is_some_and(fn) is target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("maybe", "fn", "target"),
    [
        (Some(1), is_even_async, False),
        (Some(2), is_even_async, True),
        (Empty(), is_even_async, False),
    ],
)
async def test_is_some_and_async(
    maybe: Maybe[int],
    fn: Callable[[int], Awaitable[bool]],
    target: bool,
):
    assert (await maybe.is_some_and_async(fn)) == target


def test_some_expect():
    obj = object()

    assert Some(obj).expect("must be obj") is obj


def test_empty_expect():
    what = "something"

    with pytest.raises(ValueError) as exc_info:
        Empty().expect(what)

    assert what in str(exc_info)


def test_some_unwrap():
    obj = object()

    assert Some(obj).unwrap() is obj


def test_empty_unwrap():
    with pytest.raises(ValueError) as exc_info:
        Empty().unwrap()

    assert "must be some" in str(exc_info)


@pytest.mark.parametrize(
    ("maybe", "default", "target"),
    [
        (Some(1), 0, 1),
        (Empty(), 0, 0),
    ],
)
def test_unwrap_or(maybe: Maybe[int], default: int, target: int):
    assert maybe.unwrap_or(default) == target


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(1), 1),
        (Empty(), None),
    ],
)
def test_unwrap_or_none(maybe: Maybe[int], target: int | None):
    assert maybe.unwrap_or_none() == target


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(0), 1),
        (Empty(), None),
    ],
)
def test_map(maybe: Maybe[int], target: int | None):
    assert maybe.map(add, 1).unwrap_or_none() == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some(0), 1),
        (Empty(), None),
    ],
)
async def test_map_async(maybe: Maybe[int], target: int | None):
    assert (await maybe.map_async(add_async, 1).unwrap_or_none()) == target


@pytest.mark.parametrize(
    ("maybe", "default", "target"),
    [
        (Some(0), 0, 1),
        (Empty(), 0, 0),
    ],
)
def test_map_or(maybe: Maybe[int], default: int, target: int):
    assert maybe.map_or(default, add, 1) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("maybe", "default", "target"),
    [
        (Some(0), 0, 1),
        (Empty(), 0, 0),
    ],
)
async def test_map_or_async(maybe: Maybe[int], default: int, target: int):
    assert (await maybe.map_or_async(default, add_async, 1).unwrap()) == target


@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some({}), {"key": "value"}),
        (Empty(), None),
    ],
)
def test_inspect(maybe: Maybe[dict], target: dict | None):
    assert maybe.inspect(mapping.value.set, "key", "value").unwrap_or_none() == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("maybe", "target"),
    [
        (Some({}), {"key": "value"}),
        (Empty(), None),
    ],
)
async def test_inspect_async(maybe: Maybe[dict], target: dict | None):
    assert (
        await maybe.inspect_async(set_async, "key", "value").unwrap_or_none()
    ) == target


@pytest.mark.parametrize(
    ("data", "target"),
    [
        ({}, Some(None)),
        ({"key": "value"}, Some("value")),
    ],
)
def test_wraps(data: dict, target: Maybe[str | None]):
    maybe_get = Maybe.wraps(dict.get)

    assert maybe_get(data, "key") == target


@pytest.mark.parametrize(
    ("data", "target"),
    [
        ({}, Empty()),
        ({"key": "value"}, Some("value")),
    ],
)
def test_wraps_optional(data: dict, target: Maybe[str | None]):
    maybe_get = Maybe.wraps_optional(dict.get)

    assert maybe_get(data, "key") == target


@pytest.mark.parametrize(
    ("left_maybe", "right_maybe", "target"),
    [
        (Some(object()), Some(object()), False),
        (Some(1), Some(2), False),
        (Some(1), Some(1), True),
        (Some(1), Empty(), False),
        (Empty(), Some(1), False),
    ],
)
def test_eq(left_maybe: Maybe[Any], right_maybe: Maybe[Any], target: Any):
    result = left_maybe == right_maybe

    assert result is target
