import pytest

from pypeline.pipeline import Pipeline
from pypeline.pointfree.casting import as_type, as_type_maybe


class User: ...


class Admin(User): ...


def test_as_type():
    admin_user = Pipeline(Admin()).then(as_type(User))
    assert isinstance(admin_user, Admin)
    assert isinstance(admin_user, User)

    with pytest.raises(ValueError):
        Pipeline(User()).then(as_type(Admin))


def test_as_type_maybe():
    assert Pipeline(Admin()).then(as_type_maybe(User)).is_some()
    assert Pipeline(User()).then(as_type_maybe(Admin)).is_empty()
