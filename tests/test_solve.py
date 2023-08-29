import logging
import webbrowser
from pathlib import Path

import numpy as np

from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence, SquareGroove


def flow_stress(self: RollPass.Profile):
    return 50e6 * (1 + self.strain) ** 0.2 * self.roll_pass.strain_rate ** 0.1


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    with RollPass.Profile.flow_stress(flow_stress):

        in_profile = Profile.round(
            diameter=30e-3,
            temperature=1200 + 273.15,
            material=["C45", "steel"],
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
                    rotational_frequency=1,
                    neutral_point=-20e-3
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

        try:
            sequence.solve(in_profile)
        finally:
            print("\nLog:")
            print(caplog.text)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report)
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
