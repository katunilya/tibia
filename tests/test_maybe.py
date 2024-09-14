import pytest

from tests.conftest import add, empty_if_less_than, multiply, none_if_less_than
from tibia.maybe import Empty, Maybe, Some
from tibia.pipeline import Pipeline


@pytest.mark.parametrize(
    ("maybe", "is_some", "is_empty"),
    [
        (Some(1), True, False),
        (Empty(), False, True),
    ],
)
def test_maybe_is(maybe: Maybe, is_some, is_empty):
    assert maybe.is_some() == is_some
    assert maybe.is_empty() == is_empty


@pytest.mark.parametrize(
    ("constructor", "value", "target_type"),
    [
        (Maybe.from_optional, None, Empty),
        (Maybe.from_optional, 1, Some),
        (Maybe.from_value, None, Some),
        (Maybe.from_value, 1, Some),
    ],
)
def test_maybe_construct(constructor, value, target_type):
    assert isinstance(constructor(value), target_type)


@pytest.mark.parametrize(
    "unwrap_function",
    [
        Maybe.unwrap,
        Maybe.unwrap_as_pipeline,
    ],
)
def test_unwraps_raises_error(unwrap_function):
    maybe = Maybe.from_optional(None)

    with pytest.raises(ValueError, match="Maybe is Empty"):
        unwrap_function(maybe)


def test_unwrap():
    maybe = Maybe.from_optional(1)

    assert maybe.unwrap() == 1

    pipeline = maybe.unwrap_as_pipeline()

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == 1


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (1, 1),
        (None, None),
    ],
)
def test_unwrap_as_optional(value, target):
    assert Maybe.from_optional(value).unwrap_as_optional() == target


@pytest.mark.parametrize(
    ("value", "other", "target"),
    [
        (1, 10, 1),
        (None, 10, 10),
    ],
)
def test_unwrap_or(value, other, target):
    assert Maybe.from_optional(value).unwrap_or(other) == target


@pytest.mark.parametrize(
    ("value", "func", "args", "kwargs", "target"),
    [
        (1, lambda x, y: x + y, (1, 2), {}, 1),
        (None, lambda x, y: x + y, (1, 2), {}, 3),
    ],
)
def test_unwrap_or_compute(value, func, args, kwargs, target):
    assert Maybe.from_optional(value).unwrap_or_compute(func, *args, **kwargs) == target


@pytest.mark.parametrize(
    ("value", "other", "target"),
    [
        (1, 10, 1),
        (None, 10, 10),
    ],
)
def test_unwrap_or_as_pipeline(value, other, target):
    pipeline = Maybe.from_optional(value).unwrap_or_as_pipeline(other)

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == target


@pytest.mark.parametrize(
    ("value", "func", "args", "kwargs", "target"),
    [
        (1, lambda x, y: x + y, (1, 2), {}, 1),
        (None, lambda x, y: x + y, (1, 2), {}, 3),
    ],
)
def test_unwrap_or_compute_as_pipeline(value, func, args, kwargs, target):
    pipeline = Maybe.from_optional(value).unwrap_or_compute_as_pipeline(
        func, *args, **kwargs
    )

    assert isinstance(pipeline, Pipeline)
    assert pipeline.unwrap() == target


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (None, None),
        (0, None),
        (1, None),
        (4, 50),
    ],
)
def test_maybe(value, target):
    result = (
        Maybe.from_optional(value)
        .map(add, 1)
        .map(multiply, 10)
        .map_safe(none_if_less_than, 15)
        .apply(empty_if_less_than, 30)
        .unwrap_as_optional()
    )

    assert result == target


@pytest.mark.parametrize(
    ("value", "other", "target"),
    [
        (1, 2, 1),
        (None, 2, 2),
    ],
)
def test_recover_with(value, other, target):
    assert Maybe.from_optional(value).recover_with(other).unwrap() == target


@pytest.mark.parametrize(
    ("value", "func", "args", "kwargs", "target"),
    [(1, lambda x, y: x + y, (1, 2), {}, 1), (None, lambda x, y: x + y, (1, 2), {}, 3)],
)
def test_recover_with_compute(value, func, args, kwargs, target):
    assert (
        Maybe.from_optional(value).recover_with_compute(func, *args, **kwargs).unwrap()
        == target
    )
