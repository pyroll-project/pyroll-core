import logging
from pathlib import Path

import numpy as np

from pyroll.core import (
    Profile,
    Roll,
    RollPass,
    SquareGroove,
    CircularOvalGroove,
    PassSequence
)

in_profile = Profile.from_groove(
    groove=SquareGroove(
        usable_width=21.54e-3,
        tip_depth=10.6e-3,
        r1=5e-3,
        r2=3e-3
    ),
    filling=0.97,
    gap=3e-3,
    temperature=1200 + 273.15,
    strain=0,
    material=["C45", "steel"],
    flow_stress=100e6,
    density=7.5e3,
    specific_heat_capcity=690,
)


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    sequence = PassSequence(
        [
            RollPass(
                label="Oval",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=4.43e-3,
                        r1=6e-3,
                        r2=25.5e-3
                    ),
                    nominal_radius=320,
                ),
                velocity=1,
                gap=2e-3,
            )

        ]
    )


    sequence.solve(in_profile)

    assert np.isclose(sequence.out_profile.width, sequence.out_profile.cross_section.width)
