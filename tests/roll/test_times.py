import logging
from pathlib import Path

import numpy as np

from pyroll.core import Profile, Roll, RollPass, FlatGroove


# noinspection DuplicatedCode
def test_contact_and_idle_time(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.box(
        height=5.8e-3,
        width=5.8e-3,
        corner_radius=2e-3,
        temperature=1000 + 273.15,
        material=["AISI 304", "steel"],
        length=1,
        flow_stress=100e6
    )

    rp = RollPass(
        label="Flat I",
        roll=Roll(
            groove=FlatGroove(
                usable_width=10e-3,
            ),
            nominal_radius=217e-3,
        ),
        velocity=4,
        gap=5e-3,
    )

    try:
        rp.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    assert np.isclose(rp.roll.contact_length, 13.2e-3, atol=1e-3)
    assert np.isclose(rp.roll.contact_time, 3.3e-3, atol=1e-3)
    assert np.isclose(rp.roll.idle_time, 0.338, atol=1e-3)
