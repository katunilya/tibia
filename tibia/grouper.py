from dataclasses import dataclass, field
from typing import Callable, Hashable, Iterable, Mapping, Self

from tibia.pairs import Pairs


@dataclass(slots=True)
class Grouper[_TKey: Hashable, _TValue]:
    default: _TKey
    _groups: dict[_TKey, Callable[[_TValue], bool]] = field(
        init=False,
        default_factory=dict,
    )

    def add_group(self, label: _TKey, predicate: Callable[[_TValue], bool]) -> Self:
        self._groups[label] = predicate
        return self

    def match(self, value: _TValue) -> _TKey:
        for _label, _predicate in self._groups.items():
            if _predicate(value):
                return _label

        return self.default

    def group(self, values: Iterable[_TValue]) -> Mapping[_TKey, Iterable[_TValue]]:
        result = dict[_TKey, list[_TValue]]()

        for _value in values:
            _label = self.match(_value)
            if _label not in result:
                result[_label] = []

            result[_label].append(_value)

        return result

    def group_as_pairs(
        self, values: Iterable[_TValue]
    ) -> Pairs[_TKey, Iterable[_TValue]]:
        return Pairs(self.group(values))
