import pyroll.core as pr
from pyroll.core import Profile as BaseProfile


class DummyProcessor(pr.Unit):
    def __init__(self, number):
        self._number = number
        self.label = f"Dummy {number}"

    def solve(self, in_profile: BaseProfile) -> BaseProfile:
        in_profile.dummy = self._number
        return in_profile


def test_pre_processor_add():
    def _dummy_processor_factory(u: pr.Unit):
        return DummyProcessor(42)

    pr.Unit.pre_processors.append(_dummy_processor_factory)

    u = pr.Unit("dummy_unit", duration=0)
    p = pr.Profile.round(radius=1)

    p = u.solve(p)

    assert p.dummy == 42
    assert u.in_profile.dummy == 42

    pr.Unit.pre_processors.clear()


def test_pre_processor_add_two():
    def _dummy_processor_factory42(u: pr.Unit):
        return DummyProcessor(42)

    def _dummy_processor_factory21(u: pr.Unit):
        return DummyProcessor(21)

    pr.Unit.pre_processors.append(_dummy_processor_factory42)
    pr.Unit.pre_processors.append(_dummy_processor_factory21)

    u = pr.Unit("dummy_unit", duration=0)
    p = pr.Profile.round(radius=1)

    p = u.solve(p)

    assert p.dummy == 21
    assert u.in_profile.dummy == 21

    pr.Unit.pre_processors.clear()


def test_pre_processor_add_derived():
    def _dummy_processor_factory42(u: pr.Unit):
        return DummyProcessor(42)

    def _dummy_processor_factory21(u: pr.Unit):
        return DummyProcessor(21)

    pr.Unit.pre_processors.append(_dummy_processor_factory42)
    pr.Rotator.pre_processors.append(_dummy_processor_factory21)

    u = pr.Rotator("dummy_unit", rotation=0)
    p = pr.Profile.round(radius=1)

    p = u.solve(p)

    assert p.dummy == 21
    assert u.in_profile.dummy == 21

    pr.Unit.pre_processors.clear()
    pr.Rotator.pre_processors.clear()
