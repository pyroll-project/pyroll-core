import numpy as np

from pyroll.core import Shear, PassSequence, Profile


def test_shear_cut():
    ip = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        length=10,
        density=7.5e3,
        specific_heat_capacity=690,
    )

    shear = Shear(label="Shear 1",
                  velocity=1,
                  length=5,
                  cut_length=5)

    shear.solve(ip)

    assert np.isclose(shear.out_profile.length, 5)
