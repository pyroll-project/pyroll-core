import logging
from pathlib import Path

import numpy as np

from pyroll.core import Profile, Roll, RollPass, CircularOvalGroove


# noinspection DuplicatedCode
def test_cartesian_positions(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        length=1,
        flow_stress=100e6
    )

    rp = RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        gap=2e-3,
    )

    try:
        rp.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    assert np.isclose(rp.in_profile.x, -rp.roll.contact_length)
    assert np.isclose(rp.out_profile.x, 0)


def test_cylindrical_positions(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        length=1,
        flow_stress=100e6
    )

    rp = RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        gap=2e-3,
    )

    rp.solve(in_profile)

    assert np.isclose(rp.in_profile.longitudinal_angle, rp.roll.entry_angle)
    assert np.isclose(rp.out_profile.longitudinal_angle, rp.roll.exit_angle)
