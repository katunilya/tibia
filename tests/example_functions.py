from typing import Any

from pypeline.utils import curry_first


@curry_first
def add(x: int, y: int):
    return x + y


@curry_first
def multiply(x: int, y: int):
    return x * y


@curry_first
def subtract(x: int, y: int):
    return x - y


@curry_first
def divide(x: int, y: int):
    return x // y


@curry_first
async def add_async(x: int, y: int):
    return x + y


@curry_first
async def multiply_async(x: int, y: int):
    return x * y


@curry_first
async def subtract_async(x: int, y: int):
    return x - y


@curry_first
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
