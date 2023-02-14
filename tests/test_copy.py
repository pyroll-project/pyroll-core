import copy
import logging
import webbrowser
from pathlib import Path

import numpy as np

from pyroll.core import RollPass, Roll, Unit, CircularOvalGroove, Profile, PassSequence, Transport, RoundGroove, \
    HookHost

in_profile = Profile.round(
    diameter=30e-3,
    temperature=1200 + 273.15,
    strain=0,
    material=["C45", "steel"],
    flow_stress=100e6,
    length=1,
)

sequence = PassSequence([
    RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
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
                r2=12.5e-3,
                depth=11.5e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
    Transport(
        label="II => III",
        duration=1
    ),
    RollPass(
        label="Oval III",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=6e-3,
                r1=6e-3,
                r2=35e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
])


def test_copy():
    copied_sequence = copy.copy(sequence)

    for unit, copied_unit in zip(sequence, copied_sequence):
        if isinstance(unit, HookHost):
            assert id(unit) == id(copied_unit)
        else:
            for sub_unit, copied_subunit in zip(unit, copied_unit):
                assert id(sub_unit) == id(copied_subunit)


def test_deepcopy():
    copied_sequence = copy.deepcopy(sequence)

    for unit, copied_unit in zip(sequence, copied_sequence):
        if isinstance(unit, HookHost):
            assert id(unit) != id(copied_unit)
        else:
            for sub_unit, copied_subunit in zip(unit, copied_unit):
                assert id(sub_unit) != id(copied_subunit)


def test_solve_copied(tmp_path: Path, caplog):
    sequence = PassSequence([
        RollPass(
            label="Oval I",
            roll=Roll(
                groove=CircularOvalGroove(
                    depth=8e-3,
                    r1=6e-3,
                    r2=40e-3
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
    ])

    copied_sequence = copy.deepcopy(sequence)

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    def fake_roll_torque_plugin(self: RollPass.Roll):
        fake_torque_value = 10000
        return fake_torque_value

    hf = RollPass.Roll.roll_torque.add_function(fake_roll_torque_plugin)

    try:
        copied_sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)
        RollPass.Roll.roll_torque.remove_function(hf)

    assert sequence[0] is not copied_sequence[0]
    assert not np.isclose(sequence[0].roll.roll_torque, copied_sequence[0].roll.roll_torque)
