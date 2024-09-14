from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Concatenate, Type, cast

from tibia.pipeline import Pipeline


class Result[_TOk, _TErr: Exception]:
    _value: _TOk | _TErr

    @staticmethod
    def ok[_TInputOk, _TInputErr: Exception](
        value: _TInputOk, _: Type[_TInputErr] = Exception
    ) -> Result[_TInputOk, _TInputErr]:
        return Ok(value)  # pragma: no cover

    @staticmethod
    def err[_TInputOk, _TInputErr: Exception](
        _: Type[_TInputOk], value: _TInputErr
    ) -> Result[_TInputOk, _TInputErr]:
        return Err(value)  # pragma: no cover

    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        return isinstance(self, Err)

    def as_ok(self) -> Ok[_TOk]:
        if isinstance(self, Err):
            raise ValueError("Cannot cast Result to Ok: Result is Err")

        return cast(Ok[_TOk], self)

    def as_err(self) -> Err[_TErr]:
        if isinstance(self, Ok):
            raise ValueError("Cannot cast Result to Err: Result is Ok")

        return cast(Err[_TErr], self)

    def unwrap(self) -> _TOk:
        if isinstance(self, Ok):
            return self._value

        raise ValueError("Result is Err") from cast(Err[_TErr], self)._value

    def unwrap_or(self, other: _TOk) -> _TOk:
        return self._value if isinstance(self, Ok) else other

    def unwrap_or_compute[**_ParamSpec](
        self,
        other: Callable[_ParamSpec, _TOk],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> _TOk:
        return self._value if isinstance(self, Ok) else other(*args, **kwargs)

    def unwrap_as_pipeline(self) -> Pipeline[_TOk]:
        return Pipeline(self.unwrap())

    def unwrap_or_as_pipeline(self, other: _TOk) -> Pipeline[_TOk]:
        return Pipeline(self.unwrap_or(other))

    def unwrap_or_compute_as_pipeline[**_ParamSpec](
        self,
        func: Callable[_ParamSpec, _TOk],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Pipeline[_TOk]:
        return Pipeline(self.unwrap_or_compute(func, *args, **kwargs))

    def map[_TReturn, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TOk, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Result[_TReturn, _TErr]:
        if isinstance(self, Ok):
            return Ok(func(self._value, *args, **kwargs))

        return cast(Result[_TReturn, _TErr], self)

    def map_safe[_TReturn, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TOk, _ParamSpec], _TReturn],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Result[_TReturn, _TErr | Exception]:
        if isinstance(self, Ok):
            try:
                return Ok(func(self._value, *args, **kwargs))
            except Exception as exc:
                return Err(exc)

        return cast(Result[_TReturn, _TErr | Exception], self)

    def apply[_TReturnOk, _TReturnErr: Exception, **_ParamSpec](
        self,
        func: Callable[Concatenate[_TOk, _ParamSpec], Result[_TReturnOk, _TReturnErr]],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Result[_TReturnOk, _TErr | _TReturnErr]:
        if isinstance(self, Ok):
            return func(self._value, *args, **kwargs)

        return cast(Result[_TReturnOk, _TErr], self)

    def recover_with(self, value: _TOk) -> Result[_TOk, _TErr]:
        return self if isinstance(self, Ok) else Ok(value)

    def recover_with_compute[**_ParamSpec](
        self,
        func: Callable[_ParamSpec, _TOk],
        *args: _ParamSpec.args,
        **kwargs: _ParamSpec.kwargs,
    ) -> Result[_TOk, _TErr]:
        return self if isinstance(self, Ok) else Ok(func(*args, **kwargs))


@dataclass(slots=True)
class Ok[_TOk](Result[_TOk, Any]):
    _value: _TOk

    def as_result[_TErr: Exception](
        self, _: Type[_TErr] = Exception
    ) -> Result[_TOk, _TErr]:
        return cast(Result[_TOk, _TErr], self)  # pragma: no cover


@dataclass(slots=True)
class Err[_TErr: Exception](Result[Any, _TErr]):
    _value: _TErr

    def as_result[_TOk](self, _: Type[_TOk]) -> Result[_TOk, _TErr]:
        return cast(Result[_TOk, _TErr], self)  # pragma: no cover

    def unwrap_err(self) -> _TErr:
        return self._value  # pragma: no cover


type ExcResult[_TOk] = Result[_TOk, Exception]
