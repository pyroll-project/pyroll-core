import pytest
from pyroll.core import Unit, Profile


@pytest.fixture
def unit_instance():
    return Unit(duration=1)


@pytest.fixture
def profile_instance():
    return Profile.round(1)


def init_fun(self):
    self.test_var = 42


def test_additional_inits_add(unit_instance, profile_instance):
    Unit.additional_inits.append(init_fun)

    assert not getattr(unit_instance, "test_var", None)

    unit_instance.solve(profile_instance)

    assert getattr(unit_instance, "test_var") == 42
