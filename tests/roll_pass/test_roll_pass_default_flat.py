import logging
from pathlib import Path
from pyroll.core import Profile, Roll, RollPass, FlatGroove

roll_barrel_width = 350e-3


# noinspection DuplicatedCode
def test_cartesian_positions(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.box(
        height=15e-3, width=150e-3, temperature=1200 + 273.15, material=["C45", "steel"], length=1, flow_stress=100e6
    )

    rp = RollPass(
        label="Test-Flat",
        roll=Roll(
            barrel_width=roll_barrel_width,
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3,
        ),
        gap=2e-3,
    )

    try:
        rp.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    assert isinstance(rp.roll.groove, FlatGroove)
    assert rp.roll.groove.usable_width == roll_barrel_width
