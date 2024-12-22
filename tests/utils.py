import asyncio
import time
from typing import Mapping


def add(x: int, y: int) -> int:
    return x + y


async def add_async(x: int, y: int) -> int:
    await asyncio.sleep(0.05)

    return x + y


def add_with_sleep(x: int, y: int) -> int:
    time.sleep(0.05)

    return x + y


async def set_async[K, V](mapping: Mapping[K, V], key: K, value: V) -> None:
    await asyncio.sleep(0.05)

    mapping[key] = value


def is_even(value: int) -> bool:
    return value % 2 == 0


async def is_even_async(number: int) -> bool:
    await asyncio.sleep(0.05)

    return number % 2 == 0


async def get_async[K, V](
    mapping: Mapping[K, V],
    key: K,
    default: V | None = None,
) -> V | None:
    await asyncio.sleep(0.05)

    return mapping.get(key, default)
