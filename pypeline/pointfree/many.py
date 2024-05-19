from typing import Iterable


def join[_TValue](acc: list[_TValue], next: Iterable[_TValue]) -> list[_TValue]:
    acc.extend(next)
    return acc
