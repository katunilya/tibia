from inspect import isgenerator
from typing import Callable

import pytest

from tests.utils import add, is_even
from tibia import iterable


def test_map(numbers: list[int]):
    result_gen = iterable.lazy.map(numbers, add, 1)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [add(x, 1) for x in numbers]


def test_inspect():
    iterable_ = [{"x": i} for i in range(10)]

    def set_0(item: dict[str, int]) -> None:
        item["x"] = 0

    result_gen = iterable.lazy.inspect(iterable_, set_0)
    assert isgenerator(result_gen)

    result = list(result_gen)

    assert isinstance(result, list)
    assert result == [{"x": 0} for _ in range(10)]


def test_filter(numbers: list[int]):
    result_gen = iterable.lazy.filter(numbers, is_even)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [x for x in numbers if is_even(x)]


def test_skip_while(numbers: list[int]):
    result_gen = iterable.lazy.skip_while(numbers, is_even)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9]


@pytest.mark.parametrize(
    ("nums", "predicate", "target"),
    [
        ([0, 1, 2, 3, 4], lambda x: x < 10, [0, 1, 2, 3, 4]),
        ([0, 1, 2, 3, 4], lambda x: x < 3, [0, 1, 2]),
        ([0, 1, 2, 3, 4], lambda x: x > 10, []),
    ],
)
def test_take_while(
    nums: list[int], predicate: Callable[[int], int], target: list[int]
):
    result_gen = iterable.lazy.take_while(nums, predicate)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == target


def test_join():
    result_gen = iterable.lazy.join([[0], [1, 2, 3], [4, 5]])

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [0, 1, 2, 3, 4, 5]
