import asyncio
from typing import Any

import pytest

from tests.utils import add, add_async, is_even, is_even_async, set_async
from tibia import mapping
from tibia.future_result import FutureResult, safe, safe_from, wraps
from tibia.result import Err, Ok, Result
from tibia.utils import identity_async


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), True),
        (Err("err"), False),
    ],
)
async def test_is_ok(result: Result, target: bool):
    assert (await FutureResult(identity_async(result)).is_ok()) is target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Ok(2), True),
        (Err("err"), False),
    ],
)
async def test_is_ok_and(result: Result, target: bool):
    assert await FutureResult(identity_async(result)).is_ok_and(is_even) is target


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
    assert (
        await FutureResult(identity_async(result)).is_ok_and_async(is_even_async)
    ) is target


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
async def test_is_ok_or(result: Result, target: bool):
    assert await FutureResult(identity_async(result)).is_ok_or(is_even) == target


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
    assert (
        await FutureResult(identity_async(result)).is_ok_or_async(is_even_async)
    ) == target


@pytest.mark.asyncio
async def test_ok_expect():
    obj = object()

    assert (await FutureResult(identity_async(Ok(obj))).expect("object")) == obj


@pytest.mark.asyncio
async def test_err_expect():
    what = "something"

    with pytest.raises(ValueError) as exc_info:
        await FutureResult(identity_async(Err("err"))).expect(what)

    assert what in str(exc_info)


@pytest.mark.asyncio
async def test_ok_unwrap():
    obj = object()

    assert await FutureResult(identity_async(Ok(obj))).unwrap() == obj


@pytest.mark.asyncio
async def test_err_unwrap():
    with pytest.raises(ValueError) as exc_info:
        await FutureResult(identity_async(Err("err"))).unwrap()

    assert "must be ok" in str(exc_info)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 1),
        (Err(1), 0, 0),
    ],
)
async def test_unwrap_or(result: Result, default: int, target: int):
    assert await FutureResult(identity_async(result)).unwrap_or(default) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result)).map(add, 1).unwrap_or(default)
        == target
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map_async(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result))
        .map_async(add_async, 1)
        .unwrap_or(default)
    ) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map_or(result: Result[int, int], default: int, target: int):
    assert await FutureResult(identity_async(result)).map_or(default, add, 1) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 2),
        (Err(1), 0, 0),
    ],
)
async def test_map_or_async(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result)).map_or_async(default, add_async, 1)
    ) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok({}), {}, {"key": "value"}),
        (Err({}), {}, {}),
    ],
)
async def test_inspect(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result))
        .inspect(mapping.value.set, "key", "value")
        .unwrap_or(default)
        == target
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
        await FutureResult(identity_async(result))
        .inspect_async(set_async, "key", "value")
        .unwrap_or(default)
    ) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "target"),
    [
        (Ok(1), False),
        (Err(1), True),
    ],
)
async def test_is_err(result: Result, target: bool):
    assert await FutureResult(identity_async(result)).is_err() == target


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
async def test_is_err_and(result: Result, target: bool):
    assert await FutureResult(identity_async(result)).is_err_and(is_even) == target


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
    assert (
        await FutureResult(identity_async(result)).is_err_and_async(is_even_async)
    ) == target


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
async def test_is_err_or(result: Result, target: bool):
    assert await FutureResult(identity_async(result)).is_err_or(is_even) == target


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
    assert (
        await FutureResult(identity_async(result)).is_err_or_async(is_even_async)
    ) == target


@pytest.mark.asyncio
async def test_ok_expect_err():
    what = "something"
    with pytest.raises(ValueError) as exc_info:
        await FutureResult(identity_async(Ok(1))).expect_err(what)

    assert what in str(exc_info)


@pytest.mark.asyncio
async def test_err_expect_err():
    obj = object()

    assert await FutureResult(identity_async(Err(obj))).expect_err("err") is obj


@pytest.mark.asyncio
async def test_ok_unwrap_err():
    with pytest.raises(ValueError) as exc_info:
        await FutureResult(identity_async(Ok(1))).unwrap_err()

    assert "must be err" in str(exc_info)


@pytest.mark.asyncio
async def test_err_unwrap_err():
    obj = object()

    assert await FutureResult(identity_async(Err(obj))).unwrap_err() is obj


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 1),
    ],
)
async def test_unwrap_err_or(result: Result, default: int, target: int):
    assert await FutureResult(identity_async(result)).unwrap_err_or(default) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result))
        .map_err(add, 1)
        .unwrap_err_or(default)
        == target
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err_async(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result))
        .map_err_async(add_async, 1)
        .unwrap_err_or(default)
    ) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err_or(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result)).map_err_or(default, add, 1) == target
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Ok(1), 0, 0),
        (Err(1), 0, 2),
    ],
)
async def test_map_err_or_async(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result)).map_err_or_async(
            default, add_async, 1
        )
    ) == target


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("result", "default", "target"),
    [
        (Err({}), {}, {"key": "value"}),
        (Ok({}), {}, {}),
    ],
)
async def test_inspect_err(result: Result[int, int], default: int, target: int):
    assert (
        await FutureResult(identity_async(result))
        .inspect_err(mapping.value.set, "key", "value")
        .unwrap_err_or(default)
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
        await FutureResult(identity_async(result))
        .inspect_err_async(set_async, "key", "value")
        .unwrap_err_or(default)
    ) == target


@pytest.mark.asyncio
async def test_wraps():
    wraps_add = FutureResult.wraps(add_async)

    result = await wraps_add(1, 1)

    assert isinstance(result, Ok)
    assert result == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exceptions",
    [
        [],
        [KeyError],
    ],
)
async def test_safe(exceptions: list[Exception]):
    @FutureResult.safe(*exceptions)
    async def safe_get_key(d: dict, k: Any) -> Any:
        await asyncio.sleep(0.05)

        return d[k]

    result = safe_get_key({}, "key")

    err = await result.expect_err("KeyError")
    assert isinstance(err, KeyError)


@pytest.mark.asyncio
async def test_wraps_new():
    wraps_add = wraps(add_async)

    result = await wraps_add(1, 1)

    assert isinstance(result, Ok)
    assert result == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exceptions",
    [
        [],
        [KeyError],
    ],
)
async def test_safe_from(exceptions: list[Exception]):
    @safe_from(*exceptions)
    async def safe_get_key(d: dict, k: Any) -> Any:
        await asyncio.sleep(0.05)

        return d[k]

    result = safe_get_key({}, "key")

    err = await result.expect_err("KeyError")
    assert isinstance(err, KeyError)


@pytest.mark.asyncio
async def test_safe_new():
    @safe
    async def safe_get_key(d: dict, k: Any) -> Any:
        await asyncio.sleep(0.05)

        return d[k]

    result = safe_get_key({}, "key")

    err = await result.expect_err("KeyError")
    assert isinstance(err, KeyError)
