from pyroll.core import CircularOvalGroove, RoundGroove, Roll, Profile, RollPass, Transport, SwedishOvalGroove

# initial profile
in_profile = Profile.round(
    radius=24e-3,
    temperature=1200 + 273.15,
    strain=0,
    material="C45",
    flow_stress=100e6
)

transport_duration = 2  # average time to feed workpiece into next pass

# pass sequence
sequence = [
    RollPass(
        label="K 02/001 - 1",
        roll=Roll(
            groove=SwedishOvalGroove(
                r1=6e-3,
                r2=26e-3,
                ground_width=38e-3,
                usable_width=60e-3,
                depth=7.25e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=4.5,
        gap=13.5e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 05/001 - 2",
        roll=Roll(
            groove=RoundGroove(
                r1=4e-3,
                r2=18e-3,
                depth=17.5e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=4.75,
        gap=1.5e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 02/001 - 3",
        roll=Roll(
            groove=SwedishOvalGroove(
                r1=6e-3,
                r2=26e-3,
                ground_width=38e-3,
                usable_width=60e-3,
                depth=7.25e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.1,
        gap=1.5e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 05/002 - 4",
        roll=Roll(
            groove=RoundGroove(
                r1=4e-3,
                r2=13.5e-3,
                depth=12.5e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.3,
        gap=1e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 03/001 - 5",
        roll=Roll(
            groove=CircularOvalGroove(
                r1=6e-3,
                r2=38e-3,
                depth=4e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.1,
        gap=6e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 05/003 - 6",
        roll=Roll(
            groove=RoundGroove(
                r1=3e-3,
                r2=10e-3,
                depth=9e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.3,
        gap=2e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 03/001 - 7",
        roll=Roll(
            groove=CircularOvalGroove(
                r1=6e-3,
                r2=38e-3,
                depth=4e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.1,
        gap=1e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 05/004 - 8",
        roll=Roll(
            groove=RoundGroove(
                r1=2e-3,
                r2=7.5e-3,
                depth=5.5e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.3,
        gap=4.2e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="K 03/002 - 9",
        roll=Roll(
            groove=CircularOvalGroove(
                r1=6e-3,
                r2=21.2e-3,
                depth=2.5e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.1,
        gap=4.2e-3,
    ),
    Transport(
        duration=transport_duration
    ), RollPass(
        label="K 05/005 - 10",
        roll=Roll(
            groove=RoundGroove(
                r1=0.5e-3,
                r2=6e-3,
                depth=4e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=9.3,
        gap=4.6e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="F1 - K 3/50",
        roll=Roll(
            groove=CircularOvalGroove(
                r1=2.5e-3,
                r2=12.5e-3,
                depth=2.9e-3
            ),
            nominal_radius=107.5e-3,
        ),
        velocity=2.25,
        gap=2e-3,
    ),
    Transport(
        duration=transport_duration
    ),
    RollPass(
        label="F2 - K9/24",
        roll=Roll(
            groove=RoundGroove(
                r1=0.5e-3,
                r2=5.1e-3,
                depth=4.25e-3
            ),
            nominal_radius=107.5e-3,
        ),
        velocity=2.8,
        gap=1.4e-3,
    ), Transport(
        duration=transport_duration
    ),
    RollPass(
        label="F3 - K3/51",
        roll=Roll(
            groove=CircularOvalGroove(
                r1=2.5e-3,
                r2=11e-3,
                depth=1.07e-3
            ),
            nominal_radius=107.5e-3,
        ),
        velocity=3.75,
        gap=2.1e-3,
    ), Transport(
        duration=transport_duration
    ),
    RollPass(
        label="F4 - K9/23",
        roll=Roll(
            groove=RoundGroove(
                r1=0.5e-3,
                r2=4.08e-3,
                depth=3.25e-3
            ),
            nominal_radius=85e-3,
        ),
        velocity=4.4,
        gap=1.4e-3,
    ),
]
