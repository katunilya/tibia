from tibia.maybe import Maybe
from tibia.result import Result


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


def divide(x: int, y: int) -> int:
    return x // y


def subtract(x: int, y: int) -> int:
    return x - y


async def add_async(x: int, y: int) -> int:
    return x + y


async def multiply_async(x: int, y: int) -> int:
    return x * y


async def divide_async(x: int, y: int) -> int:
    return x // y


async def subtract_async(x: int, y: int) -> int:
    return x - y


def none_if_less_than(value: int, limit: int) -> int | None:
    return None if value < limit else value


def empty_if_less_than(value: int, limit: int) -> Maybe[int]:
    return Maybe.from_optional(None if value < limit else value)


def raise_if_less_than(value: int, limit: int) -> int:
    if value < limit:
        raise ValueError("Value %s must be more than %s", value, limit)

    return value


def err_if_less_than(value: int, limit: int) -> Result[int, ValueError]:
    if value < limit:
        return Result.err(
            int, ValueError("Value %s must be more than %s", value, limit)
        )

    return Result.ok(value, ValueError)
