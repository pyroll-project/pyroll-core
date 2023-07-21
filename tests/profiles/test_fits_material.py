import pytest

from pyroll.core import Profile


def test_fits_material_str():
    p = Profile(material="tesTmAt")

    assert p.fits_material("TestmaT")


def test_fits_material_list():
    p = Profile(material=["Mat1", "maT2"])

    assert p.fits_material("mAt1")
    assert p.fits_material("mAt2")


def test_fits_material_tuple():
    p = Profile(material=("Mat1", "maT2"))

    assert p.fits_material("mAt1")
    assert p.fits_material("mAt2")


def test_fits_material_set():
    p = Profile(material={"Mat1", "maT2"})

    assert p.fits_material("mAt1")
    assert p.fits_material("mAt2")


def test_fits_material_value_error_scalar():
    p = Profile(material=1234)

    with pytest.raises(ValueError):
        p.fits_material("abc")


def test_fits_material_value_error_collection():
    p = Profile(material=["1", 2, 3, 4])

    with pytest.raises(ValueError):
        p.fits_material("abc")
