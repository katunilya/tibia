from inspect import isgenerator

from tests.iterable.utils import is_even_with_sleep
from tests.utils import add_with_sleep
from tibia import iterable


def test_map():
    result_gen = iterable.threaded.map([0, 1, 2, 3, 4], add_with_sleep, 1)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert set(result) == {1, 2, 3, 4, 5}


def test_inspect():
    iterable_ = [{"x": i} for i in range(10)]

    def set_0(item: dict[str, int]) -> None:
        item["x"] = 0

    result_gen = iterable.threaded.inspect(iterable_, set_0)
    assert isgenerator(result_gen)

    result = list(result_gen)

    assert isinstance(result, list)
    assert result == [{"x": 0} for _ in range(10)]


def test_filter():
    result_gen = iterable.threaded.filter([0, 1, 2, 3, 4], is_even_with_sleep)

    assert isgenerator(result_gen)

    result = list(result_gen)

    assert set(result) == {0, 2, 4}
