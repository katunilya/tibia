from dataclasses import dataclass
from functools import reduce
from types import GeneratorType
from typing import Callable, Iterable

from pypeline.pipeline import Pipeline


@dataclass(slots=True)
class Many[_TValue]:
    value: Iterable[_TValue]

    def unwrap(self):
        return self.value

    def unwrap_as_pipeline(self) -> Pipeline[Iterable[_TValue]]:
        return Pipeline(self.value)

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

    def compute(self):
        if isinstance(self.value, (GeneratorType, map, filter)):
            return Many([v for v in self.value])  # type: ignore

        return Many(self.value)
