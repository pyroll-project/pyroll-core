from pyroll.core import PassSequence, RollPass, CircularOvalGroove, Transport, RoundGroove, Roll
import pytest


# noinspection DuplicatedCode
def test_pass_sequence_indexing():
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

    assert sequence["Oval III"] == sequence[4]
    assert sequence["I => II"] == sequence[1]

    with pytest.raises(KeyError):
        _ = sequence["not present"]
