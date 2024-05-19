import pytest

from pypeline.pipeline import Pipeline
from pypeline.pointfree.casting import as_type


class User: ...


class Admin(User): ...


def test_as_type():
    admin_user = Pipeline(Admin()).then(as_type(User))
    assert isinstance(admin_user, Admin)
    assert isinstance(admin_user, User)

    with pytest.raises(ValueError):
        Pipeline(User()).then(as_type(Admin))
