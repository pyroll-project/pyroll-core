import pyroll.core
from pyroll.utils import for_materials


class DummyProfile:
    def __init__(self, material):
        self.material = material


def test_for_materials_single():
    def dummy_func(profile):
        return 1

    dec_func = for_materials("testmat1", "testmat2")(dummy_func)

    assert dec_func(DummyProfile("testmat1")) == 1
    assert dec_func(DummyProfile("testmat2")) == 1
    assert dec_func(DummyProfile("wrong_mat")) is None


def test_for_materials_multi():
    def dummy_func(profile):
        return 1

    dec_func = for_materials("testmat1", "testmat2")(dummy_func)

    assert dec_func(DummyProfile(["testmat1", "wrong_mat"])) == 1
    assert dec_func(DummyProfile(["testmat2", "wrong_mat"])) == 1
    assert dec_func(DummyProfile(["testmat1", "testmat2"])) == 1
    assert dec_func(DummyProfile(["wrong_mat"])) is None
