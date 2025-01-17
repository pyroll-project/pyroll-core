import numpy as np

from pyroll.core import Profile


def test_mass_per_meter():
    p = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        length=1,
        density=7.5e3,
        specific_heat_capacity=690,
    )

    assert np.isclose(p.mass_per_meter, 5.292, atol=1e-3)
