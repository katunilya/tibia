from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class Predicate[_TValue]:
    value: Callable[[_TValue], bool]

    @staticmethod
    def returns(func: Callable[[_TValue], bool]):
        return Predicate[_TValue](func)

    @staticmethod
    def all(*funcs: Callable[[_TValue], bool]):
        def _predicate(v: _TValue):
            return all(f(v) for f in funcs)

        return Predicate[_TValue](_predicate)

    @staticmethod
    def any(*funcs: Callable[[_TValue], bool]):
        def _predicate(v: _TValue):
            return any(f(v) for f in funcs)

        return Predicate[_TValue](_predicate)

    @staticmethod
    def when(
        predicate: bool | Callable[[_TValue], bool], func: Callable[[_TValue], _TValue]
    ) -> Callable[[_TValue], _TValue]:
        def _when(v: _TValue):
            condition = predicate(v) if isinstance(predicate, Callable) else predicate

            if condition:
                return func(v)

            return v

        return _when

    @staticmethod
    def when_or[_TResult](
        predicate: bool | Callable[[_TValue], bool],
        func: Callable[[_TValue], _TResult],
        other: _TResult,
    ) -> Callable[[_TValue], _TResult]:
        def _when(v: _TValue):
            condition = predicate(v) if isinstance(predicate, Callable) else predicate

            if condition:
                return func(v)

            return other

        return _when

    def unwrap(self):
        return self.value

    def and_also(self, func: Callable[[_TValue], bool]):
        def _predicate(v: _TValue):
            return self.value(v) and func(v)

        return Predicate[_TValue](_predicate)

    def or_else(self, func: Callable[[_TValue], bool]):
        def _predicate(v: _TValue):
            return self.value(v) or func(v)

        return Predicate[_TValue](_predicate)

    def __call__(self, value: _TValue) -> bool:
        return self.value(value)
