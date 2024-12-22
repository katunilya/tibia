from copy import deepcopy

import pytest

from tibia import Value, mapping


def test_map(dict_data: dict[int, str]):
    result = mapping.value.map(dict_data, len)

    assert result == {key: len(value) for key, value in dict_data.items()}


def test_filter(dict_data: dict[int, str]):
    result = mapping.value.filter(dict_data, lambda x: x == "Jane")

    assert result == {key: value for key, value in dict_data.items() if value == "Jane"}


def test_iterate(dict_data: dict[int, str]):
    result = Value(dict_data).map(mapping.value.iterate).map(list).unwrap()

    assert result == list(dict_data.values())


def test_set(dict_data: dict[int, str]):
    key, value = 3, "Ben"
    result = (
        Value(dict_data).map(deepcopy).inspect(mapping.value.set, key, value).unwrap()
    )

    assert result == {**dict_data, key: value}


def test_get(dict_data: dict[int, str]):
    result = mapping.value.get(dict_data, 1)

    assert result == dict_data[1]


def test_get_or(dict_data: dict[int, str]):
    result = mapping.value.get_or(dict_data, -1, "NO")

    assert result == "NO"


@pytest.mark.parametrize(
    ("key", "is_some"),
    [
        (1, True),
        (-1, False),
    ],
)
def test_maybe_get(dict_data: dict[int, str], key: str, is_some: bool):
    result = mapping.value.maybe_get(dict_data, key)

    assert result.is_some() == is_some
