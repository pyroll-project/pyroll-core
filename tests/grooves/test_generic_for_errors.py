import pytest

from pyroll.core import GenericElongationGroove


def test_initialization_error_non_positive():
    with pytest.raises(ValueError) as exc_info:
        obj = GenericElongationGroove(r1=-1e-3,
                                      r2=1e-3,
                                      r3=1e-3,
                                      r4=1e-3,
                                      flank_angle=1e-3,
                                      usable_width=1e-3,
                                      ground_width=1e-3,
                                      depth=1e-3,
                                      alpha3=1e-3,
                                      alpha4=1e-3,
                                      indent=1e-3,
                                      even_ground_width=1e-3
                                      )
    assert str(exc_info.value) == "Groove arguments have to be non-negative."


def test_initialization_error_to_many_given_values():
    with pytest.raises(TypeError) as exc_info:
        obj = GenericElongationGroove(r1=1e-3,
                                      r2=1e-3,
                                      r3=1e-3,
                                      r4=1e-3,
                                      flank_angle=1e-3,
                                      usable_width=1e-3,
                                      ground_width=1e-3,
                                      depth=1e-3,
                                      alpha3=1e-3,
                                      alpha4=1e-3,
                                      indent=1e-3,
                                      even_ground_width=1e-3
                                      )
    assert str(exc_info.value) == "Exactly three of usable_width, ground_width, flank_angle and depth must be given."
