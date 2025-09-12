import logging
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import pyroll.core
from shapelysmooth import chaikin_smooth

pyroll.core.Config.PROFILE_CONTOUR_REFINEMENT = 50
from pyroll.core import Profile, Roll, RollPass, PassSequence, BoxGroove, Rotator, root_hooks

def width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    return self.roll_pass.in_profile.width * self.roll_pass.draught ** -0.5

# noinspection DuplicatedCode
def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    with RollPass.OutProfile.width(width):
        root_hooks.add(RollPass.OutProfile.width)
        root_hooks.add(Rotator.OutProfile.width)
        in_profile = Profile.box(
            height=180e-3,
            width=180e-3,
            corner_radius=5e-3,
            flow_stress=100e6,
            temperature=1180 + 273.15,
            material=["C45", "steel"],
            length=1,
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="BX1",
                    roll=Roll(
                        groove=BoxGroove(depth=43.5e-3, r1=12e-3, r2=18e-3, usable_width=215e-3, flank_angle=72),
                        nominal_diameter=655e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3,
                    ),
                    gap=53e-3,
                )
            ]
        )

        try:
            sequence.solve(in_profile)
        finally:
            print("\nLog:")
            print(caplog.text)
            root_hooks.remove_last(RollPass.OutProfile.width)
            root_hooks.remove_last(Rotator.OutProfile.width)


    points = np.array(list(sequence.out_profile.cross_section.exterior.coords))
    fig, ax = plt.subplots()
    ax.plot(*sequence[0].out_profile.cross_section.boundary.xy)
    ax.scatter(points[:,0], points[:,1])
    fig.show()
