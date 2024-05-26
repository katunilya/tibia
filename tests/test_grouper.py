import pytest

from tibia.grouper import Grouper
from tibia.pairs import Pairs


@pytest.fixture()
def example_grouper():
    return (
        Grouper[str, int]("other")
        .add_group("positive", lambda x: x > 0)
        .add_group("negative", lambda x: x < 0)
    )


@pytest.mark.parametrize(
    "value, target_label",
    [
        (-100, "negative"),
        (0, "other"),
        (100, "positive"),
    ],
)
def test_match(value: int, target_label: str, example_grouper: Grouper[str, int]):
    assert example_grouper.match(value) == target_label


def test_group_by(example_grouper: Grouper[str, int]):
    _values = range(-100, 100 + 1)

    _grouped_values = example_grouper.group(_values)

    assert isinstance(_grouped_values, dict)
    assert "positive" in _grouped_values
    assert "negative" in _grouped_values
    assert "other" in _grouped_values
    assert len(list(_grouped_values["positive"])) == 100
    assert len(list(_grouped_values["negative"])) == 100
    assert len(list(_grouped_values["other"])) == 1


def test_group_by_as_pairs(example_grouper: Grouper[str, int]):
    _values = range(-100, 100 + 1)

    _pairs = example_grouper.group_as_pairs(_values)

    assert isinstance(_pairs, Pairs)
