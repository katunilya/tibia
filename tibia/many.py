from dataclasses import dataclass
from functools import reduce
from types import GeneratorType
from typing import Any, Callable, Hashable, Iterable, cast

from tibia.pairs import Pairs
from tibia.pipeline import Pipeline


@dataclass(slots=True)
class Many[_TValue]:
    value: Iterable[_TValue]

    def unwrap(self):
        return self.value

    def unwrap_as_pipeline(self) -> Pipeline[Iterable[_TValue]]:
        return Pipeline(self.value)

    def unwrap_as_pairs[_TKey: Hashable, _TNewValue](
        self, func: Callable[[_TValue], tuple[_TKey, _TNewValue]]
    ) -> Pairs[_TKey, _TNewValue]:
        result = dict[_TKey, _TNewValue]()

        for v in self.value:
            _key, _value = func(v)
            result[_key] = _value

        return Pairs(result)

    def map_values[_TResult](self, func: Callable[[_TValue], _TResult]):
        return Many([func(v) for v in self.value])

    def map_values_lazy[_TResult](self, func: Callable[[_TValue], _TResult]):
        return Many((func(v) for v in self.value))

    def skip_values(self, num: int):
        if num < 0:
            raise ValueError(f"cannot skip {num} values")

        return Many([v for i, v in enumerate(self.value) if i >= num])

    def skip_values_lazy(self, num: int):
        if num < 0:
            raise ValueError(f"cannot skip {num} values")

        return Many((v for i, v in enumerate(self.value) if i >= num))

    def take_values(self, num: int):
        if num < 0:
            raise ValueError(f"cannot take {num} values")

        return Many([v for i, v in enumerate(self.value) if i < num])

    def take_values_lazy(self, num: int):
        if num < 0:
            raise ValueError(f"cannot take {num} values")

        return Many((v for i, v in enumerate(self.value) if i < num))

    def filter_values(self, func: Callable[[_TValue], bool]):
        return Many([v for v in self.value if func(v)])

    def filter_values_lazy(self, func: Callable[[_TValue], bool]):
        return Many((v for v in self.value if func(v)))

    def reduce_values(self, func: Callable[[_TValue, _TValue], _TValue]):
        return reduce(func, self.value)

    def reduce_values_to[_TResult](
        self, func: Callable[[_TResult, _TValue], _TResult], initial: _TResult
    ):
        return reduce(func, self.value, initial)

    def group_values_by[_TKey: Hashable](self, grouper: Callable[[_TValue], _TKey]):
        result = dict[_TKey, list[_TValue]]()

        for v in self.value:
            key = grouper(v)
            if key not in result:  # pragma: no cover
                result[key] = []

            result[key].append(v)

        return Pairs(result)

    def order_values_by(
        self, *, key: Callable[[_TValue], Any] | None = None, reverse: bool = False
    ):
        if key is not None:
            return Many(sorted(self.value, key=key, reverse=reverse))

        return Many(sorted(self.value, reverse=reverse))  # type: ignore

    def order_values_by_inplace(
        self, key: Callable[[_TValue], Any] | None = None, reverse: bool = False
    ):
        values = cast(list[_TValue], self.compute_values().unwrap())

        if key:
            values.sort(key=key, reverse=reverse)
        else:
            values.sort(reverse=reverse)  # type: ignore

        return Many(values)

    def compute_values(self):
        if isinstance(self.value, (GeneratorType, map, filter)):
            return Many([v for v in self.value])  # type: ignore

        return Many(self.value)

    def map[_TNewValue](
        self, func: Callable[[Iterable[_TValue]], Iterable[_TNewValue]]
    ):
        return Many(func(self.value))

    def then[_TNewValue](
        self, func: Callable[[Iterable[_TValue]], Iterable[_TNewValue]]
    ):
        return func(self.value)

    def unwrap_as_list(self) -> list[_TValue]:
        if isinstance(self.value, list):
            return self.value

        return list(self.value)
