import pytest

from tests.conftest import add, err_if_less_than, multiply, raise_if_less_than
from tibia.pipeline import Pipeline
from tibia.result import Err, Ok, Result


@pytest.mark.parametrize(
    ("result", "is_ok", "is_err"),
    [
        (Result.ok(1), True, False),
        (Result.err(int, ValueError()), False, True),
    ],
)
def test_result_is(result: Result, is_ok, is_err):
    assert result.is_ok() == is_ok
    assert result.is_err() == is_err


@pytest.mark.parametrize(
    ("result", "as_function", "match"),
    [
        (
            Result.err(int, ValueError()),
            Result.as_ok,
            "Cannot cast Result to Ok: Result is Err",
        ),
        (
            Result.ok(1),
            Result.as_err,
            "Cannot cast Result to Err: Result is Ok",
        ),
    ],
)
def test_result_as_raises_error(result, as_function, match):
    with pytest.raises(ValueError, match=match):
        as_function(result)


@pytest.mark.parametrize(
    ("result", "as_function", "target_type"),
    [
        (Result.ok(1), Result.as_ok, Ok),
        (Result.err(int, ValueError()), Result.as_err, Err),
    ],
)
def test_result_as(result, as_function, target_type):
    assert isinstance(as_function(result), target_type)


@pytest.mark.parametrize(
    "unwrap_function",
    [
        Result.unwrap,
        Result.unwrap_as_pipeline,
    ],
)
def test_unwrap_raises(unwrap_function):
    with pytest.raises(ValueError, match="Result is Err") as exc_info:
        unwrap_function(Result.err(int, Exception("inner exception")))

    assert exc_info.value.__cause__ is not None
    assert exc_info.value.__cause__.args == ("inner exception",)


def test_unwrap():
    assert Result.ok(1).unwrap() == 1


def test_unwrap_as_pipeline():
    pipeline = Result.ok(1).unwrap_as_pipeline()

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 1


@pytest.mark.parametrize(
    ("result", "other", "target"),
    [
        (Result.ok(1), 10, 1),
        (Result.err(int, Exception()), 10, 10),
    ],
)
def test_unwrap_or(result: Result, other, target):
    assert result.unwrap_or(other) == target


@pytest.mark.parametrize(
    ("result", "func", "args", "kwargs", "target"),
    [
        (Result.ok(1), lambda x, y: x + y, (1, 2), {}, 1),
        (Result.err(int, Exception()), lambda x, y: x + y, (1, 2), {}, 3),
    ],
)
def test_unwrap_or_compute(result: Result, func, args, kwargs, target):
    assert result.unwrap_or_compute(func, *args, **kwargs) == target


@pytest.mark.parametrize(
    ("result", "other", "target"),
    [
        (Result.ok(1), 10, 1),
        (Result.err(int, Exception()), 10, 10),
    ],
)
def test_unwrap_or_as_pipeline(result: Result, other, target):
    pipeline = result.unwrap_or_as_pipeline(other)

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == target


@pytest.mark.parametrize(
    ("result", "func", "args", "kwargs", "target"),
    [
        (Result.ok(1), lambda x, y: x + y, (1, 2), {}, 1),
        (Result.err(int, Exception()), lambda x, y: x + y, (1, 2), {}, 3),
    ],
)
def test_unwrap_or_compute_as_pipeline(result: Result, func, args, kwargs, target):
    pipeline = result.unwrap_or_compute_as_pipeline(func, *args, **kwargs)

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == target


@pytest.mark.parametrize(
    ("result", "other", "target"),
    [
        (Result.err(int, Exception()), -1, -1),
        (Result.ok(0), -1, -1),
        (Result.ok(1), -1, -1),
        (Result.ok(4), -1, 50),
    ],
)
def test_result(result: Result, other, target):
    _result = (
        result.map(add, 1)
        .map(multiply, 10)
        .map_safe(raise_if_less_than, 15)
        .apply(err_if_less_than, 30)
        .unwrap_or(other)
    )

    assert _result == target


@pytest.mark.parametrize(
    ("result", "other", "target"),
    [
        (Result.ok(1), -1, 1),
        (Result.err(int, Exception()), -1, -1),
    ],
)
def test_result_recover_with(result: Result, other, target):
    assert result.recover_with(other).unwrap() == target


@pytest.mark.parametrize(
    ("result", "func", "args", "kwargs", "target"),
    [
        (Result.err(int, Exception()), (lambda x, y: x + y), (1, 2), {}, 3),
        (Result.ok(1), (lambda x, y: x + y), (1, 2), {}, 1),
    ],
)
def test_result_recover_with_compute(result: Result, func, args, kwargs, target):
    assert result.recover_with_compute(func, *args, **kwargs).unwrap() == target
