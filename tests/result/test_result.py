from typing import cast

import pytest

from pypeline.maybe import Maybe
from pypeline.pipeline import Pipeline
from pypeline.result import AsyncResult, Err, Ok, result_returns
from tests.example_functions import add, add_async, can_raise_exception


def test_is():
    assert Ok(0).is_ok() is True
    assert Err(None).is_ok() is False
    assert Ok(0).is_err() is False
    assert Err(None).is_err() is True


def test_unwrap():
    assert Ok(0).unwrap() == 0

    with pytest.raises(ValueError):
        Err(None).unwrap()


def test_unwrap_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert Ok(0).unwrap_or(other) == 0
    assert Ok(0).unwrap_or(other_func) == 0
    assert Err(None).unwrap_or(other) == other
    assert Err(None).unwrap_or(other_func) == other_func()


def test_unwrap_as_pipeline():
    pipeline = Ok(0).unwrap_as_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 0

    with pytest.raises(ValueError):
        Err(None).unwrap_as_pipeline()


def test_unwrap_as_pipeline_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    pipeline = Ok(0).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 0

    pipeline = Ok(0).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 0

    pipeline = Err(None).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == other

    pipeline = Err(None).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == other_func()


def test_unwrap_as_maybe():
    maybe = Ok(0).unwrap_as_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == 0

    with pytest.raises(ValueError):
        Err(None).unwrap_as_maybe()


def test_unwrap_as_maybe_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    maybe = Ok(0).unwrap_as_maybe_or(other)
    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == 0

    maybe = Ok(0).unwrap_as_maybe_or(other_func)
    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == 0

    maybe = Err(None).unwrap_as_maybe_or(other)
    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == other

    maybe = Err(None).unwrap_as_maybe_or(other_func)
    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == other_func()


def test_map():
    assert Ok(0).map(add(1)).unwrap() == 1

    with pytest.raises(ValueError):
        Err(None).map(add(1)).unwrap()


def test_then():
    assert Ok(0).then(add(1)) == 1

    with pytest.raises(ValueError):
        Err(None).then(add(1))


def test_then_or():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert Ok(0).then_or(add(10), other) == 10
    assert Ok(0).then_or(add(10), other_func) == 10
    assert Err(None).then_or(add(10), other) == other
    assert Err(None).then_or(add(10), other_func) == other_func()


@pytest.mark.asyncio
async def test_map_async():
    async_result = Ok(0).map_async(add_async(1))

    assert isinstance(async_result, AsyncResult)
    assert await async_result.unwrap() == 1

    async_result = Err(None).map_async(add_async(1))
    assert isinstance(async_result, AsyncResult)

    with pytest.raises(ValueError):
        await async_result.unwrap()


@pytest.mark.asyncio
async def test_then_async():
    assert await Ok(0).then_async(add_async(1)) == 1

    with pytest.raises(ValueError):
        await Err(None).then_async(add_async(1))


@pytest.mark.asyncio
async def test_then_or_async():
    other = 1
    other_func = lambda: int(2)  # noqa: E731

    assert await Ok(0).then_or_async(add_async(10), other) == 10
    assert await Ok(0).then_or_async(add_async(10), other_func) == 10
    assert await Err(None).then_or_async(add_async(10), other) == other
    assert await Err(None).then_or_async(add_async(10), other_func) == other_func()


def test_result_returns():
    _error_returns = result_returns(can_raise_exception)

    assert isinstance(_error_returns(True), Err)
    assert isinstance(_error_returns(False), Ok)


def test_otherwise():
    _err = Err(0).as_result(str).otherwise(add(1))
    assert isinstance(_err, Err)
    assert _err.value == 1

    _ok = Ok(0).as_result(int).otherwise(add(1))

    assert isinstance(_ok, Ok)
    assert cast(Ok[int], _ok).value == 0


@pytest.mark.asyncio
async def test_otherwise_async():
    _err = await (Err(0).as_result(str).otherwise_async(add_async(1))).value
    assert isinstance(_err, Err)
    assert _err.value == 1

    _ok = await (Ok(0).as_result(int).otherwise_async(add_async(1))).value

    assert isinstance(_ok, Ok)
    assert cast(Ok[int], _ok).value == 0


def test_recover():
    other = ""

    _result = Err(0).as_result(str).recover(other)

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == other

    _result = Err(0).as_result(str).recover(lambda: "f")

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == "f"

    _result = Ok("str").as_result(int).recover(str)

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == "str"
    _result = Ok("str").as_result(int).recover(lambda: "f")

    assert isinstance(_result, Ok)
    assert isinstance(_result.value, str)
    assert _result.value == "str"
