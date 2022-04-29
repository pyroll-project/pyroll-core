from pyroll import Profile
from pyroll import RollPass, Transport
from pyroll import RoundGroove, CircularOvalGroove

# initial profile
in_profile = Profile(
    width=30e-3,
    height=30e-3,
    groove=RoundGroove(r1=0, r2=15e-3, depth=15e-3),
    temperature=1200 + 273.15,
    strain=0,
    material="C45",
    flow_stress=100e6
)

# pass sequence
sequence = [
    RollPass(
        label="Oval I",
        groove=CircularOvalGroove(
            depth=5e-3,
            r1=6e-3,
            r2=40e-3
        ),
        nominal_roll_radius=160,
        velocity=1,
        gap=1e-3,
    ),
    Transport(
        label="I => II",
        time=1
    ),
    RollPass(
        label="Round II",
        groove=RoundGroove(
            r1=1e-3,
            r2=9e-3,
            depth=8.5e-3
        ),
        nominal_roll_radius=160,
        velocity=1,
        gap=1e-3,
    ),
]
