from dataclasses import dataclass
from functools import reduce
from types import GeneratorType
from typing import Any, Callable, Hashable, Iterable, cast

from pypeline.pairs import Pairs
from pypeline.pipeline import Pipeline


@dataclass(slots=True)
class Many[_TValue]:
    value: Iterable[_TValue]

    def unwrap(self):
        return self.value

    def unwrap_as_pipeline(self) -> Pipeline[Iterable[_TValue]]:
        return Pipeline(self.value)

    def unwrap_as_pairs[_TKey: Hashable](
        self, grouper: Callable[[_TValue], _TKey]
    ) -> Pairs[_TKey, Iterable[_TValue]]:
        result = dict[_TKey, list[_TValue]]()

        for v in self.value:
            key = grouper(v)
            if key not in result:  # pragma: no cover
                result[key] = []

            result[key].append(v)

        return Pairs(result)

    def map[_TResult](self, func: Callable[[_TValue], _TResult]):
        return Many([func(v) for v in self.value])

    def map_lazy[_TResult](self, func: Callable[[_TValue], _TResult]):
        return Many((func(v) for v in self.value))

    def skip(self, num: int):
        if num < 0:
            raise ValueError(f"cannot skip {num} values")

        return Many([v for i, v in enumerate(self.value) if i >= num])

    def skip_lazy(self, num: int):
        if num < 0:
            raise ValueError(f"cannot skip {num} values")

        return Many((v for i, v in enumerate(self.value) if i >= num))

    def take(self, num: int):
        if num < 0:
            raise ValueError(f"cannot take {num} values")

        return Many([v for i, v in enumerate(self.value) if i < num])

    def take_lazy(self, num: int):
        if num < 0:
            raise ValueError(f"cannot take {num} values")

        return Many((v for i, v in enumerate(self.value) if i < num))

    def filter(self, func: Callable[[_TValue], bool]):
        return Many([v for v in self.value if func(v)])

    def filter_lazy(self, func: Callable[[_TValue], bool]):
        return Many((v for v in self.value if func(v)))

    def reduce(self, func: Callable[[_TValue, _TValue], _TValue]):
        return reduce(func, self.value)

    def reduce_to[_TResult](
        self, func: Callable[[_TResult, _TValue], _TResult], initial: _TResult
    ):
        return reduce(func, self.value, initial)

    def order_by(
        self, *, key: Callable[[_TValue], Any] | None = None, reverse: bool = False
    ):
        if key is not None:
            return Many(sorted(self.value, key=key, reverse=reverse))

        return Many(sorted(self.value, reverse=reverse))  # type: ignore

    def order_by_inplace(
        self, key: Callable[[_TValue], Any] | None = None, reverse: bool = False
    ):
        values = cast(list[_TValue], self.compute().unwrap())

        if key:
            values.sort(key=key, reverse=reverse)
        else:
            values.sort(reverse=reverse)  # type: ignore

        return Many(values)

    def compute(self):
        if isinstance(self.value, (GeneratorType, map, filter)):
            return Many([v for v in self.value])  # type: ignore

        return Many(self.value)
