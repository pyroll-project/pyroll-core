import pytest
import logging
from pathlib import Path


from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence


def flow_stress(self: RollPass.Profile):
    return 50e6 * (1 + self.strain) ** 0.2 * self.roll_pass.strain_rate**0.1


# noinspection DuplicatedCode
def test_by_position(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    with RollPass.Profile.flow_stress(flow_stress):
        in_profile = Profile.round(
            diameter=30e-3, temperature=1200 + 273.15, material=["C45", "steel"], length=1, position=0
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Oval I",
                    roll=Roll(
                        groove=CircularOvalGroove(depth=8e-3, r1=6e-3, r2=40e-3),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3,
                    ),
                    gap=2e-3,
                ),
                Transport(
                    label="I => II",
                    duration=1,
                ),
                RollPass(
                    label="Round II",
                    roll=Roll(
                        groove=RoundGroove(r1=1e-3, r2=12.5e-3, depth=11.5e-3),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                    ),
                    gap=2e-3,
                ),
                Transport(label="II => III", duration=1),
                RollPass(
                    label="Oval III",
                    roll=Roll(
                        groove=CircularOvalGroove(depth=6e-3, r1=6e-3, r2=35e-3),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                    ),
                    gap=2e-3,
                ),
            ]
        )

        try:
            sequence.solve(in_profile)
        finally:
            print("\nLog:")
            print(caplog.text)

    assert sequence.find_value_by_position_or_time(position=1.15, hook_name="temperature") == 1473.15

    with pytest.raises(ValueError) as exc_info:
        sequence.find_value_by_position_or_time(position=1.15, hook_name="test")
    assert str(exc_info.value) == ("No hook with name test found.")

    with pytest.raises(ValueError) as exc_info:
        sequence.find_value_by_position_or_time(position=10, hook_name="temperature")
    assert str(exc_info.value) == ("Coordinate index 10 out of sequence range.")
