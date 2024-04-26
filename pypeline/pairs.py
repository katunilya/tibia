from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Mapping


@dataclass(slots=True)
class Pairs[_TKey: Hashable, _TValue]:
    value: Mapping[_TKey, _TValue]

    def unwrap(self):
        return self.value

    def values(self) -> Iterable[_TValue]:
        return list(self.value.values())

    def lazy_values(self) -> Iterable[_TValue]:
        for v in self.value.values():
            yield v

    def keys(self) -> Iterable[_TKey]:
        return list(self.value.keys())

    def lazy_keys(self) -> Iterable[_TKey]:
        for k in self.value.keys():
            yield k

    def map_values[_TNewValue](self, func: Callable[[_TValue], _TNewValue]):
        return Pairs({k: func(v) for k, v in self.value.items()})

    def map_keys[_TNewKey: Hashable](self, func: Callable[[_TKey], _TNewKey]):
        return Pairs({func(k): v for k, v in self.value.items()})

    def filter_by_value(self, func: Callable[[_TValue], bool]):
        return Pairs({k: v for k, v in self.value.items() if func(v)})

    def filter_by_key(self, func: Callable[[_TKey], bool]):
        return Pairs({k: v for k, v in self.value.items() if func(k)})

    def as_iterable(self) -> Iterable[tuple[_TKey, _TValue]]:
        return [(k, v) for k, v in self.value.items()]

    def as_lazy_iterable(self) -> Iterable[tuple[_TKey, _TValue]]:
        for k, v in self.value.items():
            yield (k, v)
