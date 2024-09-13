from inspect import isawaitable

import pytest

from tests.example_functions import add, add_async, multiply
from tibia.pipeline import Pipeline


def test_pipeline_curring():
    result = Pipeline(0).map(add, 1).map(add, 2).map(multiply, 10).then(add, 3)

    assert result == 33


@pytest.mark.asyncio
async def test_async_pipeline_curring():
    async_result = (
        Pipeline(0)
        .map_async(add_async, 1)
        .map_async(add_async, 2)
        .map(multiply, 10)
        .then_async(add_async, 3)
    )

    assert isawaitable(async_result)

    result = await async_result

    assert result == 33
