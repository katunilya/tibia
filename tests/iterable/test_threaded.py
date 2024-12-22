from inspect import isgenerator

from tests.iterable.utils import is_even_with_sleep
from tests.utils import add_with_sleep
from tibia import iterable


def test_map():
    result_gen = iterable.threaded.map([0, 1, 2, 3, 4], add_with_sleep, 1)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert set(result) == {1, 2, 3, 4, 5}


def test_filter():
    result_gen = iterable.threaded.filter([0, 1, 2, 3, 4], is_even_with_sleep)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert set(result) == {0, 2, 4}
