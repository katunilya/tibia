from copy import deepcopy

from tibia import Value, mapping


def test_map(dict_data: dict[int, str]):
    result = (
        Value(dict_data)
        .map(deepcopy)
        .map(mapping.item.map, lambda i, s: (i + 1, f"{i} {s}"))
        .unwrap()
    )

    assert result == {key + 1: f"{key} {value}" for key, value in dict_data.items()}


def test_map_to_value(dict_data: dict[int, str]):
    result = (
        Value(dict_data)
        .map(deepcopy)
        .map(mapping.item.map_to_value, lambda key, value: f"{key} {value}")
        .unwrap()
    )

    assert result == {key: f"{key} {value}" for key, value in dict_data.items()}


def test_map_to_key(dict_data: dict[int, str]):
    result = (
        Value(dict_data)
        .map(deepcopy)
        .map(mapping.item.map_to_key, lambda key, value: f"{key} {value}")
        .unwrap()
    )

    assert result == {f"{key} {value}": value for key, value in dict_data.items()}


def test_filter(dict_data: dict[int, str]):
    result = (
        Value(dict_data)
        .map(deepcopy)
        .map(mapping.item.filter, lambda key, value: key > 1 and value == "John")
        .unwrap()
    )

    assert result == {}


def test_iterate(dict_data: dict[int, str]):
    result = Value(dict_data).map(mapping.item.iterate).map(list).unwrap()

    assert result == [(key, value) for key, value in dict_data.items()]
