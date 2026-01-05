import logging
import webbrowser
from pathlib import Path

import numpy as np

from pyroll.core import Profile, Roll, AsymmetricTwoRollPass, CircularOvalGroove, PassSequence


def flow_stress(self: AsymmetricTwoRollPass.Profile):
    return 50e6 * (1 + self.strain) ** 0.2 * self.roll_pass.strain_rate ** 0.1


# noinspection DuplicatedCode
def test_solve_asymmetric(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    with AsymmetricTwoRollPass.Profile.flow_stress(flow_stress):

        in_profile = Profile.round(
            diameter=30e-3,
            temperature=1200 + 273.15,
            material=["C45", "steel"],
            length=1,
        )

        sequence = PassSequence([
            AsymmetricTwoRollPass(
                label="Oval I",
                upper_roll=Roll(
                    groove=CircularOvalGroove(
                        depth=14e-3,
                        r1=6e-3,
                        usable_width=50e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                lower_roll=Roll(
                    groove=CircularOvalGroove(
                        depth=4e-3,
                        r1=6e-3,
                        usable_width=50e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                lower_groove_rotation=90,
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
        report_file.write_text(report, encoding="utf-8")
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
