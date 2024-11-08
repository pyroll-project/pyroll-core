import logging
from pathlib import Path
import matplotlib.pyplot as plt
from shapely import equals, affinity

import numpy as np

from pyroll.core import Profile, Roll, RollPass, CircularOvalGroove

def test_techological_orientation(tmp_path: Path, caplog):
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
        orientation='v',
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

    assert equals(
        affinity.rotate(rp.out_profile.cross_section, 90, origin=(0, 0)),
        rp.out_profile.technologically_orientated_cross_section
    )
    assert equals(
        affinity.rotate(rp.contour_lines.geoms[0], 90, origin=(0, 0)),
        rp.technologically_orientated_contour_lines.geoms[0]
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(*rp.out_profile.cross_section.exterior.xy)
    ax1.plot(*rp.contour_lines.geoms[0].xy, 'black', linestyle='--')
    ax1.set_title("out_profile and contour_line")
    ax1.set_aspect('equal')
    ax1.set_ylim([-0.04, 0.04])
    ax1.set_xlim([-0.04, 0.04])
    ax2.plot(*rp.out_profile.technologically_orientated_cross_section.exterior.xy, 'red')
    ax2.plot(*rp.technologically_orientated_contour_lines.geoms[0].xy, 'black', linestyle='--')
    ax2.set_title("technologically_orientated out_profile and contour_line")
    ax2.set_aspect('equal')
    ax2.set_ylim([-0.04, 0.04])
    ax2.set_xlim([-0.04, 0.04])

    fig.show()
