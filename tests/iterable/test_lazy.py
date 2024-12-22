from inspect import isgenerator

from tests.utils import add, is_even
from tibia import iterable


def test_map(numbers: list[int]):
    result_gen = iterable.lazy.map(numbers, add, 1)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [add(x, 1) for x in numbers]


def test_filter(numbers: list[int]):
    result_gen = iterable.lazy.filter(numbers, is_even)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert result == [x for x in numbers if is_even(x)]
