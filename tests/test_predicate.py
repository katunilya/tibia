from typing import Callable

from pypeline.curry import curried
from pypeline.predicate import Predicate
from tests.example_functions import add


@curried
def is_more_then(number: int, limit: int):
    return number > limit


@curried
def is_less_then(number: int, limit: int):
    return number < limit


def test_returns():
    predicate = Predicate[int].returns(is_less_then(10))
    assert isinstance(predicate, Predicate)
    assert predicate(5) is True
    assert predicate(15) is False


def test_all():
    predicate = Predicate[int].all(is_less_then(10), is_more_then(-10))

    assert isinstance(predicate, Predicate)
    assert predicate(0) is True
    assert predicate(-20) is False
    assert predicate(20) is False


def test_any():
    predicate = Predicate[int].any(is_less_then(-10), is_more_then(10))

    assert isinstance(predicate, Predicate)
    assert predicate(0) is False
    assert predicate(-20) is True
    assert predicate(20) is True


def test_when():
    f = Predicate[int].when(is_more_then(10), add(1))
    assert f(5) == 5
    assert f(11) == 12


def test_when_or():
    f = Predicate[int].when_or(is_more_then(10), add(1), 0)
    assert f(5) == 0
    assert f(11) == 12


def test_unwrap():
    f = Predicate(is_more_then(10)).unwrap()
    assert isinstance(f, Callable)
    assert f(12) is True


def test_and_also():
    predicate = Predicate(is_more_then(-10)).and_also(is_less_then(10))

    assert isinstance(predicate, Predicate)
    assert predicate(0) is True
    assert predicate(-20) is False
    assert predicate(20) is False


def test_or_else():
    predicate = Predicate(is_more_then(10)).or_else(is_less_then(-10))

    assert isinstance(predicate, Predicate)
    assert predicate(0) is False
    assert predicate(-20) is True
    assert predicate(20) is True
