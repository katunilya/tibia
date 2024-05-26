from typing import Any

import pytest

from tibia.maybe import (
    Empty,
    Maybe,
    Some,
    maybe_as_empty,
    maybe_as_some,
    maybe_from_optional,
    maybe_is_empty,
    maybe_is_some,
    maybe_returns,
    maybe_unwrap,
)
from tibia.pipeline import Pipeline
from tibia.result import Err, Ok
from tests.example_functions import (
    add,
    add_async,
    can_return_optional,
)


def test_is():
    assert Some(0).is_some() is True
    assert Empty().is_some() is False
    assert Some(0).is_empty() is False
    assert Empty().is_empty() is True


def test_from_optional():
    assert isinstance(maybe_from_optional(0), Some)
    assert isinstance(maybe_from_optional(None), Empty)


def test_unwrap():
    assert Some(3).unwrap() == 3

    with pytest.raises(ValueError):
        Empty().unwrap()


def test_unwrap_or():
    other = 4
    other_func = lambda: int(5)  # noqa: E731

    assert Some(0).unwrap_or(other) == 0
    assert Some(0).unwrap_or(other_func) == 0
    assert Empty().unwrap_or(other) == other
    assert Empty().unwrap_or(other_func) == other_func()


@pytest.mark.parametrize("value", [3, None])
def test_unwrap_as_optional(value: Any):
    assert maybe_from_optional(value).unwrap_as_optional() == value


def test_unwrap_as_pipeline():
    value = 3

    pipeline = Some(value).unwrap_as_pipeline()

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == value

    with pytest.raises(ValueError):
        Empty().unwrap_as_pipeline()


def test_unwrap_as_pipeline_optional():
    pipeline = Some(0).unwrap_as_pipeline_optional()

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 0

    pipeline = Empty().as_maybe(int).unwrap_as_pipeline_optional()

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() is None


def test_unwrap_as_pipeline_or():
    other = 4
    other_func = lambda: 5  # noqa: E731

    pipeline = Some(3).unwrap_as_pipeline_or(other)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 3

    pipeline = Some(3).unwrap_as_pipeline_or(other_func)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 3

    assert Empty().unwrap_or(other) == other
    assert Empty().unwrap_or(other_func) == other_func()


def test_unwrap_as_result():
    result = Some(3).unwrap_as_result()

    assert isinstance(result, Ok)
    assert result.unwrap() == 3

    result = Empty().unwrap_as_result()

    assert isinstance(result, Err)
    assert isinstance(result.value, ValueError)


def test_unwrap_as_result_or():
    other = 4
    other_func = lambda: 5  # noqa: E731

    result = Some(3).unwrap_as_result_or(other)

    assert isinstance(result, Ok)
    assert result.unwrap() == 3

    result = Some(3).unwrap_as_result_or(other_func)

    assert isinstance(result, Ok)
    assert result.unwrap() == 3

    result = Empty().unwrap_as_result_or(other)

    assert isinstance(result, Ok)
    assert result.unwrap() == other

    result = Empty().unwrap_as_result_or(other_func)

    assert isinstance(result, Ok)
    assert result.unwrap() == other_func()


def test_map():
    assert Some(0).map(add(1)).unwrap() == 1

    with pytest.raises(ValueError):
        Empty().as_maybe(int).map(add(1)).unwrap()


def test_then():
    assert Some(0).then(add(1)) == 1

    with pytest.raises(ValueError):
        Empty().then(add(1))


def test_then_or():
    other = 1
    other_func = lambda: 2  # noqa: E731

    assert Some(0).then_or(add(1), other) == 1
    assert Some(0).then_or(add(1), other_func) == 1
    assert Empty().then_or(add(1), other) == other
    assert Empty().then_or(add(1), other_func) == other_func()


@pytest.mark.asyncio
async def test_map_async_some():
    assert await Some(0).map_async(add_async(1)).unwrap() == 1


@pytest.mark.asyncio
async def test_map_async_empty():
    with pytest.raises(ValueError):
        await Empty().map_async(add_async(1)).unwrap()


@pytest.mark.asyncio
async def test_then_async_some():
    assert await Some(0).then_async(add_async(1)) == 1


@pytest.mark.asyncio
async def test_then_async_empty():
    with pytest.raises(ValueError):
        await Empty().then_async(add_async(1))


@pytest.mark.asyncio
async def test_then_or_async_some():
    other = 1
    other_func = lambda: 2  # noqa: E731

    assert await Some(0).then_or_async(add_async(10), other) == 10
    assert await Some(0).then_or_async(add_async(10), other_func) == 10


@pytest.mark.asyncio
async def test_then_or_async_empty():
    other = 1
    other_func = lambda: 2  # noqa: E731

    assert await Empty().then_or_async(add_async(10), other) == other
    assert await Empty().then_or_async(add_async(10), other_func) == other_func()


def test_optional_safe():
    assert isinstance(maybe_returns(can_return_optional)(True), Empty)
    assert isinstance(maybe_returns(can_return_optional)(False), Some)


def test_maybe_unwrap():
    some = Some(0).as_maybe()
    assert maybe_unwrap(some) == some.unwrap()

    with pytest.raises(ValueError):
        maybe_unwrap(Empty().as_maybe(int))


@pytest.mark.parametrize("m, result", [(Some(0), True), (Empty(), False)])
def test_maybe_is_some(m: Maybe[Any], result: bool):
    assert maybe_is_some(m) == m.is_some() == result


@pytest.mark.parametrize("m, result", [(Some(0), False), (Empty(), True)])
def test_maybe_is_empty(m: Maybe[Any], result: bool):
    assert maybe_is_empty(m) == m.is_empty() == result


def test_maybe_as_some():
    some = Some(0).as_maybe()

    assert maybe_as_some(some) == some.as_some() == some

    with pytest.raises(ValueError):
        Empty().as_maybe(int).as_some()


def test_maybe_as_empty():
    empty = Empty().as_maybe(int)

    assert maybe_as_empty(empty) == empty.as_empty() == empty

    with pytest.raises(ValueError):
        Some(0).as_maybe().as_empty()
