import numpy as np
from pyroll.core import  Roll, RollPass, FalseRoundGroove, CircularOvalGroove

rp1 = RollPass(
    label="Oval I",
    roll=Roll(groove=CircularOvalGroove(depth=15.5e-3, r1=2e-3, r2=60.5e-3),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)

rp2 = RollPass(
    label="FR I",
    roll=Roll(groove=FalseRoundGroove(depth=20.5e-3, r1=2e-3, r2=23.75e-3, flank_angle=60),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)

rp3 = RollPass(
    label="Oval II",
    roll=Roll(groove=CircularOvalGroove(depth=12.25e-3, r1=2e-3, r2=39.28e-3),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=5.5e-3,
)

rp4 = RollPass(
    label="FR II",
    roll=Roll(groove=FalseRoundGroove(depth=15.25e-3, r1=2e-3, r2=18e-3,flank_angle=60),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=5.5e-3,
)


working_radii = np.asarray([rp1.roll.working_radius, rp2.roll.working_radius, rp3.roll.working_radius, rp4.roll.working_radius])
working_radii_analytical_lee = np.asarray([142.02e-3, 136.32e-3, 144.66e-3, 141.28e-3])


def test_working_radius_too_lee_paper():
    print("\n")
    print("Working radii current implementation: ", working_radii)
    print("Working radii Lee analytical model: ", working_radii_analytical_lee)
