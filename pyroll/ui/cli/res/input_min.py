from pyroll import Profile, Roll
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
        roll=Roll(
            groove=CircularOvalGroove(
                depth=5e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=1e-3,
    ),
    Transport(
        label="I => II",
        duration=1
    ),
    RollPass(
        label="Round II",
        roll=Roll(
            groove=RoundGroove(
                r1=1e-3,
                r2=9e-3,
                depth=8.5e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=1e-3,
    ),
]
