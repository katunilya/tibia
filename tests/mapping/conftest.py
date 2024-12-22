import pytest


@pytest.fixture
def dict_data() -> dict[int, str]:
    return {1: "John", 2: "Jane"}
