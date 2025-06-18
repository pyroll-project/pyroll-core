import logging
import webbrowser
from pathlib import Path

import numpy as np

from pyroll.core import (
    Profile,
    Roll,
    RollPass,
    CircularOvalGroove,
    PassSequence,
    root_hooks,
    Rotator,
)


def width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    return self.roll_pass.in_profile.width * self.roll_pass.draught ** -0.5


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    with RollPass.OutProfile.width(width):
        root_hooks.add(RollPass.OutProfile.width)
        root_hooks.add(Rotator.OutProfile.width)

        in_profile = Profile.square(
            side=24e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            specific_heat_capcity=690,
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Oval",
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
                    disk_element_count=15,
                ),

            ]
        )

        try:
            sequence.solve(in_profile)
        finally:
            print("\nLog:")
            print(caplog.text)

            root_hooks.remove_last(RollPass.OutProfile.width)
            root_hooks.remove_last(Rotator.OutProfile.width)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report, encoding="utf-8")
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass

    assert not np.isclose(sequence[0].out_profile.filling_ratio, 1)