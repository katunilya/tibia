import pytest

from tibia.predicate import all_, any_, not_, when, when_or, where
from tibia.value import Value


@pytest.mark.parametrize(
    ("value", "target"),
    [
        ("", False),
        ("abc", False),
        ("abc123", True),
    ],
)
def test_all(value: str, target: bool) -> None:
    pfn = all_(
        lambda s: "a" in s,
        lambda s: "1" in s,
    )

    assert pfn(value) == target


@pytest.mark.parametrize(
    ("value", "target"),
    [
        ("", False),
        ("abc", True),
        ("abc123", True),
    ],
)
def test_any(value: str, target: bool) -> None:
    pfn = any_(
        lambda s: "a" in s,
        lambda s: "1" in s,
    )

    assert pfn(value) == target


@pytest.mark.parametrize(
    ("value", "target", "target_not"),
    [
        ("", False, True),
        ("abc", True, False),
        ("123", False, True),
    ],
)
def test_not(value: str, target: bool, target_not: bool) -> None:
    not_pnf = not_(str.__contains__, "abc")

    assert ("abc" in value) == target
    assert not_pnf(value) == target_not


@pytest.mark.parametrize(
    ("value", "target"),
    [
        ("", False),
        ("abc", True),
        ("abc123", True),
    ],
)
def test_where(value: str, target: bool) -> None:
    pfn = (
        where(str.__contains__, "a")
        .and_(str.__contains__, "b")
        .or_(str.__contains__, "c12")
        .unwrap()
    )

    assert pfn(value) == target


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (0, 0),
        (1, 2),
    ],
)
def test_when(value: int, target: int) -> None:
    result = Value(value).map(when, lambda i: i > 0, lambda i: i + 1).unwrap()

    assert result == target


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (0, "no"),
        (1, "1"),
    ],
)
def test_when_or(value: int, target: str) -> None:
    result = Value(value).map(when_or, "no", lambda i: i > 0, str).unwrap()

    assert result == target
