from tests.utils import is_even
from tibia import Value, mapping


def test_map(dict_data: dict[int, str]):
    result = mapping.key.map(dict_data, str)

    assert result == {str(key): value for key, value in dict_data.items()}


def test_filter(dict_data: dict[int, str]):
    result = mapping.key.filter(dict_data, is_even)

    assert result == {key: value for key, value in dict_data.items() if is_even(key)}


def test_iterate(dict_data: dict[int, str]):
    result = Value(dict_data).map(mapping.key.iterate).map(list).unwrap()

    assert result == list(dict_data.keys())
