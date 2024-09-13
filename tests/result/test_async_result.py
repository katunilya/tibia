import pytest

from tibia.maybe import AsyncMaybe
from tibia.pipeline import AsyncPipeline
from tibia.result import AsyncResult, Err, Ok, result_returns_async
from tests.curried_example_functions import (
    add,
    add_async,
    can_raise_exception_async,
    str_async,
)


async def ok_int_async(value: int):
    return Ok(value).with_err(Exception)


async def err_exc_async(exc: Exception = Exception()):
    return Err(exc).with_ok(int)


@pytest.mark.asyncio
async def test_unwrap():
    assert await AsyncResult(ok_int_async(0)).unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).unwrap()


@pytest.mark.asyncio
async def test_unwrap_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncResult(ok_int_async(0)).unwrap_or(other) == 0
    assert await AsyncResult(ok_int_async(0)).unwrap_or(other_func) == 0
    assert await AsyncResult(err_exc_async()).unwrap_or(other) == other
    assert await AsyncResult(err_exc_async()).unwrap_or(other_func) == other_func()


@pytest.mark.asyncio
async def test_unwrap_as_pipeline():
    pipeline = AsyncResult(ok_int_async(0)).unwrap_as_pipeline()

    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).unwrap_as_pipeline().unwrap()


@pytest.mark.asyncio
async def test_unwrap_as_pipeline_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    pipeline = AsyncResult(ok_int_async(0)).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    pipeline = AsyncResult(ok_int_async(0)).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == 0

    pipeline = AsyncResult(err_exc_async()).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == other

    pipeline = AsyncResult(err_exc_async()).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, AsyncPipeline)
    assert await pipeline.unwrap() == other_func()


@pytest.mark.asyncio
async def test_unwrap_as_maybe():
    maybe = AsyncResult(ok_int_async(0)).unwrap_as_maybe()

    assert isinstance(maybe, AsyncMaybe)
    assert await maybe.unwrap() == 0

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).unwrap_as_maybe().unwrap()


@pytest.mark.asyncio
async def test_unwrap_as_maybe_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    maybe = AsyncResult(ok_int_async(0)).unwrap_as_maybe_or(other)
    assert isinstance(maybe, AsyncMaybe)
    assert await maybe.unwrap() == 0

    maybe = AsyncResult(ok_int_async(0)).unwrap_as_maybe_or(other_func)
    assert isinstance(maybe, AsyncMaybe)
    assert await maybe.unwrap() == 0

    maybe = AsyncResult(err_exc_async()).unwrap_as_maybe_or(other)
    assert isinstance(maybe, AsyncMaybe)
    assert await maybe.unwrap() == other

    maybe = AsyncResult(err_exc_async()).unwrap_as_maybe_or(other_func)
    assert isinstance(maybe, AsyncMaybe)
    assert await maybe.unwrap() == other_func()


@pytest.mark.asyncio
async def test_map():
    assert await AsyncResult(ok_int_async(0)).map(add(1)).unwrap() == 1

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).map(add(1)).unwrap()


@pytest.mark.asyncio
async def test_then():
    assert await AsyncResult(ok_int_async(0)).then(add(1)) == 1

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).then(add(1))


@pytest.mark.asyncio
async def test_then_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncResult(ok_int_async(0)).then_or(add(10), other) == 10
    assert await AsyncResult(ok_int_async(0)).then_or(add(10), other_func) == 10
    assert await AsyncResult(err_exc_async()).then_or(add(10), other) == other
    assert (
        await AsyncResult(err_exc_async()).then_or(add(10), other_func) == other_func()
    )


@pytest.mark.asyncio
async def test_map_async():
    assert await AsyncResult(ok_int_async(0)).map_async(add_async(1)).unwrap() == 1

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).map_async(add_async(1)).unwrap()


@pytest.mark.asyncio
async def test_then_async():
    assert await AsyncResult(ok_int_async(0)).then_async(add_async(1)) == 1

    with pytest.raises(ValueError):
        await AsyncResult(err_exc_async()).then_async(add_async(1))


@pytest.mark.asyncio
async def test_then_or_async():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await AsyncResult(ok_int_async(0)).then_or_async(add_async(10), other) == 10
    assert (
        await AsyncResult(ok_int_async(0)).then_or_async(add_async(10), other_func)
        == 10
    )
    assert (
        await AsyncResult(err_exc_async()).then_or_async(add_async(10), other) == other
    )
    assert (
        await AsyncResult(err_exc_async()).then_or_async(add_async(10), other_func)
        == other_func()
    )


@pytest.mark.asyncio
async def test_result_returns_async():
    _error_returns = result_returns_async(can_raise_exception_async)

    _err = _error_returns(True)
    assert isinstance(_err, AsyncResult)
    with pytest.raises(ValueError):
        await _err.unwrap()

    _ok = _error_returns(False)
    assert isinstance(_ok, AsyncResult)
    assert await _ok.unwrap() == 0


@pytest.mark.asyncio
async def test_otherwise():
    _err = await AsyncResult(err_exc_async()).otherwise(str).value

    assert isinstance(_err, Err)
    assert isinstance(_err.value, str)
    assert _err.value == str(Exception())

    _ok = await AsyncResult(ok_int_async(0)).otherwise(str).value

    assert isinstance(_ok, Ok)
    assert isinstance(_ok.value, int)
    assert _ok.value == 0


@pytest.mark.asyncio
async def test_otherwise_async():
    _err = await AsyncResult(err_exc_async()).otherwise_async(str_async).value

    assert isinstance(_err, Err)
    assert isinstance(_err.value, str)
    assert _err.value == str(Exception())

    _ok = await AsyncResult(ok_int_async(0)).otherwise_async(str_async).value

    assert isinstance(_ok, Ok)
    assert isinstance(_ok.value, int)
    assert _ok.value == 0


@pytest.mark.asyncio
async def test_recover():
    other = ""

    _result = await AsyncResult(err_exc_async()).recover(other).value

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == other

    _result = await AsyncResult(err_exc_async()).recover(lambda: "f").value

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == "f"

    _result = await AsyncResult(ok_int_async(0)).recover(-1).value

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, int)
    assert _result.value == 0

    _result = await AsyncResult(ok_int_async(0)).recover(lambda: -1).value

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, int)
    assert _result.value == 0
