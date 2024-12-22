import math
from copy import deepcopy
from functools import reduce
from typing import Callable

import pytest

from tests.utils import add, is_even
from tibia import iterable
from tibia.value import Value


def test_map(numbers: list[int]):
    result = Value(numbers).map(deepcopy).map(iterable.map, add, 1).unwrap()

    assert isinstance(result, list)
    assert result == [add(x, 1) for x in numbers]


def test_filter(numbers: list[int]):
    result = Value(numbers).map(deepcopy).map(iterable.filter, is_even).unwrap()

    assert isinstance(result, list)
    assert result == [x for x in numbers if is_even(x)]


def test_reduce(numbers: list[int]):
    result = Value(numbers).map(iterable.reduce, add).unwrap()

    assert result == sum(numbers)


def test_reduce_to(numbers: list[int]):
    result = (
        Value(numbers)
        .map(iterable.reduce_to, lambda x, y, z: x + f"{y}-{z}", "initial", "z")
        .unwrap()
    )

    assert result == reduce(lambda x, y: x + f"{y}-z", numbers, "initial")


@pytest.mark.parametrize(
    ("nums", "key", "target"),
    [
        ([-2, -1, 0, 1, 2], lambda x: math.pow(x, 2), [0, -1, 1, -2, 2]),
        ([-3, 2, -1, 0, 1, -2, 3], None, [-3, -2, -1, 0, 1, 2, 3]),
    ],
)
def test_sort_asc(nums: list[int], key: Callable[[int], int] | None, target: list[int]):
    result = iterable.sort_asc(nums, key)

    assert result == target


@pytest.mark.parametrize(
    ("nums", "key", "target"),
    [
        ([-2, -1, 0, 1, 2], lambda x: math.pow(x, 2), [-2, 2, -1, 1, 0]),
        ([-3, 2, -1, 0, 1, -2, 3], None, [3, 2, 1, 0, -1, -2, -3]),
    ],
)
def test_sort_desc(
    nums: list[int], key: Callable[[int], int] | None, target: list[int]
):
    result = iterable.sort_desc(nums, key)

    assert result == target


@pytest.mark.parametrize(
    ("nums", "amount", "target"),
    [
        ([0, 1, 2, 3, 4], 0, []),
        ([0, 1, 2, 3, 4], 3, [0, 1, 2]),
        ([0, 1, 2, 3, 4], -3, [2, 3, 4]),
    ],
)
def test_take(nums: list[int], amount: int, target: list[int]):
    result = iterable.take(nums, amount)

    assert result == target


@pytest.mark.parametrize(
    ("nums", "default", "target"),
    [
        ([0, 1, 2, 3, 4], -1, 0),
        ([], -1, -1),
        ([], None, None),
    ],
)
def test_first(nums: list[int], default: int, target: int):
    result = iterable.first(nums, default)

    assert result == target


@pytest.mark.parametrize(
    ("nums", "amount", "target"),
    [
        ([0, 1, 2, 3, 4], 0, [0, 1, 2, 3, 4]),
        ([0, 1, 2, 3, 4], 3, [3, 4]),
        ([0, 1, 2, 3, 4], -3, [0, 1]),
    ],
)
def test_skip(nums: list[int], amount: int, target: list[int]):
    result = iterable.skip(nums, amount)

    assert result == target


def test_join():
    result = iterable.join([[0], [1, 2, 3], [4, 5]])

    assert result == [0, 1, 2, 3, 4, 5]
