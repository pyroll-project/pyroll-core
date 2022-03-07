from pyroll.core.grooves import SquareGroove, DiamondGroove, CircularOvalGroove, RoundGroove
from pyroll.core import Profile
from pyroll.core import RollPass, Transport
from numpy import pi

# initial profile
in_profile = Profile(
    width=68e-3,
    height=68e-3,
    groove=SquareGroove(r1=0, r2=3e-3, tip_angle=pi / 2, tip_depth=34e-3),
    temperature=1200 + 273.15,
    strain=0,
    material="C45",
    flow_stress=100e6
)

# mean roll radii
# in reality asymmetrical, but spreading model is not able to work with
mean_roll_radius_1_upper = (328e-3 + 324e-3) / 2 / 2
mean_roll_radius_1_lower = (324e-3 + 320e-3) / 2 / 2
mean_roll_radius_2_upper = (299e-3 + 297e-3) / 2 / 2
mean_roll_radius_2_lower = (297e-3 + 295e-3) / 2 / 2
mean_roll_radius_3_upper = (280e-3 + 278e-3) / 2 / 2
mean_roll_radius_3_lower = (278e-3 + 276e-3) / 2 / 2

transport_time = 2  # average time to feed workpiece into next pass

# pass sequence
sequence = [
    RollPass(
        label="Raute I",
        groove=DiamondGroove(
            usable_width=76.55e-3,
            tip_depth=22.1e-3,
            r1=12e-3,
            r2=8e-3
        ),
        roll_radius=mean_roll_radius_1_lower,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Quadrat II",
        groove=SquareGroove(
            usable_width=52.7e-3,
            tip_depth=25.95e-3,
            r1=8e-3,
            r2=6e-3
        ),
        roll_radius=mean_roll_radius_1_upper,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Raute III",
        groove=DiamondGroove(
            usable_width=58.3e-3,
            tip_depth=16.85e-3,
            r1=7e-3,
            r2=8e-3
        ),
        roll_radius=mean_roll_radius_1_lower,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Quadrat IV",
        groove=SquareGroove(
            usable_width=40.74e-3,
            tip_depth=20.05e-3,
            r1=7e-3,
            r2=5e-3
        ),
        roll_radius=mean_roll_radius_1_upper,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Oval V",
        groove=CircularOvalGroove(
            depth=7.25e-3,
            r1=6e-3,
            r2=44.5e-3
        ),
        roll_radius=mean_roll_radius_1_lower,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Quadrat VI",
        groove=SquareGroove(
            usable_width=29.64e-3,
            tip_depth=14.625e-3,
            r1=6e-3,
            r2=4e-3
        ),
        roll_radius=mean_roll_radius_1_upper,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Oval VII",
        groove=CircularOvalGroove(
            depth=5.05e-3,
            r1=7e-3,
            r2=33e-3
        ),
        roll_radius=mean_roll_radius_1_lower,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Quadrat VIII",
        groove=SquareGroove(
            usable_width=21.54e-3,
            tip_depth=10.6e-3,
            r1=5e-3,
            r2=3e-3
        ),
        roll_radius=mean_roll_radius_1_upper,
        velocity=1,
        gap=3e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Oval IX",
        groove=CircularOvalGroove(
            depth=4.43e-3,
            r1=6e-3,
            r2=25.5e-3
        ),
        roll_radius=mean_roll_radius_2_lower,
        velocity=1,
        gap=1e-3,
    ),
    Transport(
        time=transport_time
    ),
    RollPass(
        label="Fertigrund Xa",
        groove=RoundGroove(
            r1=2e-3,
            r2=15.8e-3 / 2,
            depth=7.65e-3
        ),
        roll_radius=mean_roll_radius_2_upper,
        velocity=1,
        gap=0.5e-3,
    ),
]
