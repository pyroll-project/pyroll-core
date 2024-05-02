import pytest
from pyroll.core import Unit, Profile


class SubClassUnit(Unit):
    pass


@pytest.fixture
def unit_instance():
    return Unit(duration=1)


@pytest.fixture
def profile_instance():
    return Profile.round(1)


def test_additional_inits_add(unit_instance, profile_instance):
    def init_fun(self):
        self.test_var = 42

    Unit.additional_inits.append(init_fun)

    assert not getattr(unit_instance, "test_var", None)

    unit_instance.solve(profile_instance)

    assert getattr(unit_instance, "test_var") == 42


def test_additional_inits_subclass(unit_instance, profile_instance):
    def init_fun(self):
        self.test_var = 42

    def init_fun2(self):
        assert self.test_var == 42  # test for base-first evaluation order
        self.test_var2 = 21

    Unit.additional_inits.append(init_fun)
    SubClassUnit.additional_inits.append(init_fun2)

    assert not getattr(unit_instance, "test_var", None)

    unit_instance.solve(profile_instance)

    assert getattr(unit_instance, "test_var") == 42
    assert not getattr(unit_instance, "test_var2", None)

    sub_instance = SubClassUnit(duration=1)

    sub_instance.solve(profile_instance)

    assert getattr(sub_instance, "test_var") == 42
    assert getattr(sub_instance, "test_var2") == 21
