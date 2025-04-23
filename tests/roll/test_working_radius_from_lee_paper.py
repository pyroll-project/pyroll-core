from pyroll.core import  Roll, RollPass, FalseRoundGroove, CircularOvalGroove

rp1 = RollPass(
    label="Oval I",
    roll=Roll(groove=CircularOvalGroove(depth=31e-3, r1=2e-3, r2=60.5e-3),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)

rp2 = RollPass(
    label="FR I",
    roll=Roll(groove=FalseRoundGroove(depth=20.5e-3, r1=2e-3, r2=20e-3, flank_angle=60),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)

rp3 = RollPass(
    label="Oval II",
    roll=Roll(groove=CircularOvalGroove(depth=31e-3, r1=2e-3, r2=60.5e-3),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)

rp4 = RollPass(
    label="FR II",
    roll=Roll(groove=CircularOvalGroove(depth=31e-3, r1=2e-3, r2=60.5e-3),
              nominal_radius=155e-3,
              rotational_frequency=1,
              ),
    gap=6.5e-3,
)


