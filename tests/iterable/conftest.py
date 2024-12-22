import pytest


@pytest.fixture
def numbers() -> list[int]:
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
