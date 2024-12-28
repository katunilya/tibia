from typing import Any, Callable

import pytest

from tests.utils import add, add_async, is_even, is_even_async, set_async
from tibia import mapping
from tibia.result import Err, Ok, Result, match_ok


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), True),
        (Err("err"), False),
    ],
)
def test_is_ok(result: Result, target: bool):
    assert result.is_ok() is target


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), True),
        (Err("err"), False),
    ],
)
def test_is_ok_and(result: Result, target: bool):
    assert result.is_ok_and(is_even) is target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), True),
        (Err("err"), False),
    ],
)
async def test_is_ok_and_async(result: Result, target: bool):
    assert (await result.is_ok_and_async(is_even_async)) is target


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), True),
        (Ok(2), True),
        (Err(1), False),
        (Err(2), True),
    ],
)
def test_is_ok_or(result: Result, target: bool):
    assert result.is_ok_or(is_even) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), True),
        (Ok(2), True),
        (Err(1), False),
        (Err(2), True),
    ],
)
async def test_is_ok_or_async(result: Result, target: bool):
    assert (await result.is_ok_or_async(is_even_async)) == target


def test_ok_expect():
    obj = object()

    assert Ok(obj).expect("object") == obj


def test_err_expect():
    what = "something"
    with pytest.raises(ValueError) as exc_info:
        Err("err").expect(what)

    assert what in str(exc_info)


def test_ok_unwrap():
    obj = object()

    assert Ok(obj).unwrap() == obj


def test_err_unwrap():
    with pytest.raises(ValueError) as exc_info:
        Err("err").unwrap()

    assert "must be ok" in str(exc_info)


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 1),
        (Err(1), 0, 0),
    ],
)
def test_unwrap_or(result: Result, default: int, target: int):
    assert result.unwrap_or(default) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
def test_map(result: Result[int, int], default: int, target: int):
    assert result.map(add, 1).unwrap_or(default) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map_async(result: Result[int, int], default: int, target: int):
    assert (await result.map_async(add_async, 1).unwrap_or(default)) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
def test_map_or(result: Result[int, int], default: int, target: int):
    assert result.map_or(default, add, 1) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map_or_async(result: Result[int, int], default: int, target: int):
    assert (await result.map_or_async(default, add_async, 1)) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok({}), {}, {"key": "value"}),
        (Err({}), {}, {}),
    ],
)
def test_inspect(result: Result[int, int], default: int, target: int):
    assert (
        result.inspect(mapping.value.set, "key", "value").unwrap_or(default) == target
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok({}), {}, {"key": "value"}),
        (Err({}), {}, {}),
    ],
)
async def test_inspect_async(result: Result[int, int], default: int, target: int):
    assert (
        await result.inspect_async(set_async, "key", "value").unwrap_or(default)
    ) == target


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Err(1), True),
    ],
)
def test_is_err(result: Result, target: bool):
    assert result.is_err() == target


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), False),
        (Err(1), False),
        (Err(2), True),
    ],
)
def test_is_err_and(result: Result, target: bool):
    assert result.is_err_and(is_even) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), False),
        (Err(1), False),
        (Err(2), True),
    ],
)
async def test_is_err_and_async(result: Result, target: bool):
    assert (await result.is_err_and_async(is_even_async)) == target


@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), True),
        (Err(1), True),
        (Err(2), True),
    ],
)
def test_is_err_or(result: Result, target: bool):
    assert result.is_err_or(is_even) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), True),
        (Err(1), True),
        (Err(2), True),
    ],
)
async def test_is_err_or_async(result: Result, target: bool):
    assert (await result.is_err_or_async(is_even_async)) == target


def test_ok_expect_err():
    what = "something"
    with pytest.raises(ValueError) as exc_info:
        Ok(1).expect_err(what)

    assert what in str(exc_info)


def test_err_expect_err():
    obj = object()

    assert Err(obj).expect_err("err") is obj


def test_ok_unwrap_err():
    with pytest.raises(ValueError) as exc_info:
        Ok(1).unwrap_err()

    assert "must be err" in str(exc_info)


def test_err_unwrap_err():
    obj = object()

    assert Err(obj).unwrap_err() is obj


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 1),
    ],
)
def test_unwrap_err_or(result: Result, default: int, target: int):
    assert result.unwrap_err_or(default) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
def test_map_err(result: Result[int, int], default: int, target: int):
    assert result.map_err(add, 1).unwrap_err_or(default) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err_async(result: Result[int, int], default: int, target: int):
    assert (await result.map_err_async(add_async, 1).unwrap_err_or(default)) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
def test_map_err_or(result: Result[int, int], default: int, target: int):
    assert result.map_err_or(default, add, 1) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err_or_async(result: Result[int, int], default: int, target: int):
    assert (await result.map_err_or_async(default, add_async, 1)) == target


@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Err({}), {}, {"key": "value"}),
        (Ok({}), {}, {}),
    ],
)
def test_inspect_err(result: Result[int, int], default: int, target: int):
    assert (
        result.inspect_err(mapping.value.set, "key", "value").unwrap_err_or(default)
        == target
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Err({}), {}, {"key": "value"}),
        (Ok({}), {}, {}),
    ],
)
async def test_inspect_err_async(result: Result[int, int], default: int, target: int):
    assert (
        await result.inspect_err_async(set_async, "key", "value").unwrap_err_or(default)
    ) == target


def test_wraps():
    wraps_add = Result.wraps(add)

    result = wraps_add(1, 1)

    assert isinstance(result, Ok)
    assert result == 2


@pytest.mark.parametrize(
    "exceptions",
    [
        [],
        [KeyError],
    ],
)
def test_safe(exceptions: list[Exception]):
    @Result.safe(*exceptions)
    def safe_get_key(d: dict, k: Any) -> Any:
        return d[k]

    result = safe_get_key({}, "key")

    err = result.expect_err("KeyError")
    assert isinstance(err, KeyError)


@pytest.mark.parametrize(
    ("left_result", "right_result", "target"),
    [
        (Ok(1), Ok(1), True),
        (Ok(1), 1, True),
        (Ok(1), Ok(2), False),
        (Ok(1), Err(1), False),
        (Ok(1), Err(2), False),
        (Err(1), Ok(1), False),
        (Err(1), 1, True),
        (Err(1), Ok(2), False),
        (Err(1), Err(1), True),
        (Err(1), Err(2), False),
    ],
)
def test_eq(left_result: Result, right_result: Result, target: bool):
    result = left_result == right_result

    assert result == target


@pytest.mark.parametrize(
    ("fns", "is_ok"),
    [
        ([lambda x: Err(x), lambda x: Err(x + 1), lambda x: Ok(x + 2)], True),
        ([lambda x: Err(x), lambda x: Err(x + 1), lambda x: Err(x + 2)], False),
    ],
)
def test_match_ok(fns: list[Callable[[int], Result[int, int]]], is_ok: bool):
    r = match_ok(*fns)(0)

    assert r.is_ok() == is_ok
