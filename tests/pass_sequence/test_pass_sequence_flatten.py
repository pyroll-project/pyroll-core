import logging
from pathlib import Path

from pyroll.core import (
    Roll,
    RollPass,
    Transport,
    RoundGroove,
    CircularOvalGroove,
    PassSequence,
)

# noinspection DuplicatedCode
def test_pass_sequence_flatten(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    sequence = PassSequence(
        [
            RollPass(
                label="Oval I",
                roll=Roll(
                    groove=CircularOvalGroove(depth=8e-3, r1=6e-3, r2=40e-3),
                    nominal_radius=160e-3,
                ),
                gap=2e-3,
            ),
            Transport(
                label="I => II",
                length=1,
            ),
        ])
    sequence_2 = PassSequence([
        RollPass(
            label="Round II",
            roll=Roll(
                groove=RoundGroove(r1=1e-3, r2=12.5e-3, depth=11.5e-3),
                nominal_radius=160e-3,
            ),
            gap=2e-3,
        ),
        Transport(label="II => III", length=1),
        RollPass(
            label="Oval III",
            roll=Roll(
                groove=CircularOvalGroove(depth=6e-3, r1=6e-3, r2=35e-3),
                nominal_radius=160e-3,
            ),
            gap=2e-3,
        ),
    ]
    )

    sequence.append(sequence_2)
    sequence.flatten()

    assert 5 == len(sequence)
    assert isinstance(sequence[2], RollPass)