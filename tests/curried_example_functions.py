from typing import Any

from tibia.curry import curried


@curried
def add(x: int, y: int):
    return x + y


@curried
def multiply(x: int, y: int):
    return x * y


@curried
def subtract(x: int, y: int):
    return x - y


@curried
def divide(x: int, y: int):
    return x // y


@curried
async def add_async(x: int, y: int):
    return x + y


@curried
async def multiply_async(x: int, y: int):
    return x * y


@curried
async def subtract_async(x: int, y: int):
    return x - y


@curried
async def divide_async(x: int, y: int):
    return x // y


def can_return_optional(do: bool):
    if do:
        return None

    return int(0)


async def can_return_optional_async(do: bool):
    if do:
        return None

    return int(0)


def can_raise_exception(do: bool):
    if do:
        raise Exception()

    return int(0)


async def can_raise_exception_async(do: bool):
    if do:
        raise Exception()

    return int(0)


async def str_async(value: Any):
    return str(value)
