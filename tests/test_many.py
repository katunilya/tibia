import random
from types import GeneratorType
from typing import Any, Callable, Generator, cast

import pytest

from tibia.many import Many
from tibia.pairs import Pairs
from tibia.pipeline import Pipeline


@pytest.fixture()
def finite_generator():
    def _finite_generator(start: int = -100, size: int = 200):
        for i in range(size):
            yield start + i

    return _finite_generator


@pytest.fixture()
def int_list():
    return list(range(-100, 100))


@pytest.fixture()
def shuffled_generator():
    def _shuffled_generator():
        for _ in range(100):
            yield random.randint(-10, 10)

    return _shuffled_generator


@pytest.fixture()
def random_int_list():
    return [random.randint(-10, 10) for _ in range(100)]


def test_unwrap(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    assert isinstance(Many(finite_generator()).unwrap(), GeneratorType)
    assert isinstance(Many(int_list).unwrap(), list)


def test_unwrap_as_pipeline(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    g = finite_generator()
    p = Many(g).unwrap_as_pipeline()
    assert isinstance(p, Pipeline)
    assert p.unwrap() == g

    p = Many(int_list).unwrap_as_pipeline()
    assert isinstance(p, Pipeline)
    assert p.unwrap() == int_list


def test_unwrap_as_pairs(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    p = Many(finite_generator()).unwrap_as_pairs(lambda x: (x - 10, x))
    assert isinstance(p, Pairs)
    assert all([isinstance(v, int) for v in p.values()])
    assert all([k == v - 10 for k, v in p.unwrap().items()])

    p = Many(int_list).unwrap_as_pairs(lambda x: (x - 10, x))
    assert isinstance(p, Pairs)
    assert all([isinstance(v, int) for v in p.values()])
    assert all([k == v - 10 for k, v in p.unwrap().items()])


def test_map_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).map_values(lambda i: i + 1).unwrap()
    assert min(r) == -99
    assert max(r) == 100

    r = Many(int_list).map_values(lambda i: i + 1).unwrap()
    assert min(r) == -99
    assert max(r) == 100


def test_map_values_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).map_values_lazy(lambda i: i + 1).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert min(r) == -99
    assert max(r) == 100

    r = Many(int_list).map_values_lazy(lambda i: i + 1).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert min(r) == -99
    assert max(r) == 100


def test_skip_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).skip_values(100).unwrap()
    assert len(cast(list[int], r)) == 100

    r = Many(int_list).skip_values(100).unwrap()
    assert len(cast(list[int], r)) == 100


def test_skip_values_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).skip_values_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100

    r = Many(int_list).skip_values_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100


def test_skip_values_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).skip_values(-1)


def test_skip_values_lazy_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).skip_values_lazy(-1)


def test_take_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).take_values(100).unwrap()
    assert len(cast(list[int], r)) == 100

    r = Many(int_list).take_values(100).unwrap()
    assert len(cast(list[int], r)) == 100


def test_take_values_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).take_values_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100

    r = Many(int_list).take_values_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100


def test_take_values_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).take_values(-1)


def test_take_values_lazy_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).take_values_lazy(-1)


def test_filter_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).filter_values(lambda x: x < 0).unwrap()
    assert isinstance(r, list)
    assert all([x < 0 for x in r])

    r = Many(int_list).filter_values(lambda x: x < 0).unwrap()
    assert isinstance(r, list)
    assert all([x < 0 for x in r])


def test_filter_values_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).filter_values_lazy(lambda x: x < 0).unwrap()
    assert isinstance(r, GeneratorType)
    assert all([x < 0 for x in r])

    r = Many(int_list).filter_values_lazy(lambda x: x < 0).unwrap()
    assert isinstance(r, GeneratorType)
    assert all([x < 0 for x in r])


def test_reduce_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).reduce_values(lambda acc, nxt: acc + nxt)
    assert isinstance(r, int)
    assert r == sum(finite_generator())

    r = Many(int_list).reduce_values(lambda acc, nxt: acc + nxt)
    assert isinstance(r, int)
    assert r == sum(int_list)


def test_reduce_values_to(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).reduce_values_to(
        lambda acc, nxt: acc + nxt, -sum(finite_generator())
    )
    assert isinstance(r, int)
    assert r == 0

    r = Many(int_list).reduce_values_to(lambda acc, nxt: acc + nxt, -sum(int_list))
    assert isinstance(r, int)
    assert r == 0


def test_group_values_by(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    p = Many(finite_generator()).group_values_by(lambda x: -x)
    assert isinstance(p, Pairs)
    assert all([isinstance(v, list) for v in p.values()])

    p = Many(int_list).group_values_by(lambda x: -x)
    assert isinstance(p, Pairs)
    assert all([isinstance(v, list) for v in p.values()])


order_by_parametrize = pytest.mark.parametrize(
    "key,reverse",
    [
        (None, False),
        (None, True),
        (lambda x: str(x), False),  # type: ignore
        (lambda x: str(x), True),  # type: ignore
    ],
)


@order_by_parametrize
def test_order_values_by(
    shuffled_generator: Callable[[], Generator[int, Any, None]],
    random_int_list: list[int],
    key: Callable[[Any], Any] | None,
    reverse: bool,
):
    r = Many(shuffled_generator()).order_values_by(key=key, reverse=reverse).unwrap()
    assert isinstance(r, list)

    r = Many(random_int_list).order_values_by(key=key, reverse=reverse).unwrap()
    assert isinstance(r, list)
    assert r == sorted(random_int_list, key=key, reverse=reverse)


@order_by_parametrize
def test_order_values_by_inplace(
    shuffled_generator: Callable[[], Generator[int, Any, None]],
    random_int_list: list[int],
    key: Callable[[Any], Any] | None,
    reverse: bool,
):
    r = (
        Many(shuffled_generator())
        .order_values_by_inplace(key=key, reverse=reverse)
        .unwrap()
    )
    assert isinstance(r, list)

    r = Many(random_int_list).order_values_by_inplace(key=key, reverse=reverse).unwrap()
    assert isinstance(r, list)
    assert id(r) == id(random_int_list)


def test_compute_values(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    assert isinstance(Many(finite_generator()).compute_values().unwrap(), list)
    assert isinstance(Many(int_list).compute_values().unwrap(), list)


def test_map(finite_generator: Callable[[], Generator[int, Any, None]]):
    iterable = Many(finite_generator()).map(lambda i: [_i + 1 for _i in i]).unwrap()

    assert isinstance(iterable, list)
    assert max(iterable) == 100
    assert min(iterable) == -99


def test_then(finite_generator: Callable[[], Generator[int, Any, None]]):
    iterable = Many(finite_generator()).then(lambda i: [_i + 1 for _i in i])

    assert isinstance(iterable, list)
    assert max(iterable) == 100
    assert min(iterable) == -99


def test_unwrap_as_list(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    many = Many(finite_generator())

    assert isinstance(many.unwrap(), Generator)
    assert isinstance(many.unwrap_as_list(), list)

    many = Many(int_list)

    assert isinstance(many.unwrap(), list)
    assert isinstance(many.unwrap_as_list(), list)


def test_unwrap_as_set():
    result = Many([1, 1, 2, 2, 3, 3, 3]).unwrap_as_set()

    assert result == {1, 2, 3}
