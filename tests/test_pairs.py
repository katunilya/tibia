from types import GeneratorType
from typing import Any, Mapping, cast

import pytest

from pypeline.pairs import Pairs


@pytest.fixture()
def mapping():
    return {x: -x for x in range(-10, 10 + 1)}


def test_unwrap(mapping: Mapping[int, int]):
    assert isinstance(Pairs(mapping).unwrap(), dict)


def test_values(mapping: Mapping[int, int]):
    values = Pairs(mapping).values()
    assert isinstance(values, list)
    assert values == [x for x in mapping.values()]


def test_values_lazy(mapping: Mapping[int, int]):
    values = Pairs(mapping).values_lazy()
    assert isinstance(values, GeneratorType)
    assert [x for x in values] == [x for x in mapping.values()]


def test_keys(mapping: Mapping[int, int]):
    keys = Pairs(mapping).keys()
    assert isinstance(keys, list)
    assert keys == [x for x in mapping.keys()]


def test_keys_lazy(mapping: Mapping[int, int]):
    keys = Pairs(mapping).keys_lazy()
    assert isinstance(keys, GeneratorType)
    assert [x for x in keys] == [x for x in mapping.keys()]


def test_map_values(mapping: Mapping[int, int]):
    values = Pairs(mapping).map_values(lambda _: 0).values()
    assert all([v == 0 for v in values])


def test_map_keys(mapping: Mapping[int, int]):
    keys = Pairs(mapping).map_keys(lambda _: 0).keys()
    assert all([v == 0 for v in keys])


def test_filter_by_values(mapping: Mapping[int, int]):
    r = Pairs(mapping).filter_by_value(lambda v: v == 0).unwrap()
    assert len(r) == 1
    assert r == {0: 0}


def test_filter_by_key(mapping: Mapping[int, int]):
    r = Pairs(mapping).filter_by_key(lambda v: v == 0).unwrap()
    assert len(r) == 1
    assert r == {0: 0}


def test_as_iterable(mapping: Mapping[int, int]):
    r = Pairs(mapping).as_iterable()
    assert all([isinstance(x, tuple) for x in r])
    assert len(cast(list[Any], r)) == len(mapping)


def test_as_iterable_lazy(mapping: Mapping[int, int]):
    r = Pairs(mapping).as_iterable_lazy()
    assert isinstance(r, GeneratorType)

    r = [x for x in r]
    assert all([isinstance(x, tuple) for x in r])
    assert len(cast(list[Any], r)) == len(mapping)
