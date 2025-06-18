import logging
import webbrowser
import numpy as np

from pathlib import Path
from pyroll.core import (
    Profile,
    Roll,
    RollPass,
    ConstrictedBoxGroove,
    PassSequence,
    root_hooks,
    Rotator,
)


def width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    return self.roll_pass.in_profile.width * self.roll_pass.draught ** -0.5


def test_solve_round_constricted_box(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    with RollPass.OutProfile.width(width):
        root_hooks.add(RollPass.OutProfile.width)
        root_hooks.add(Rotator.OutProfile.width)

        in_profile = Profile.round(
            diameter=19.5e-3,
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
                    label="Constricted Box",
                    roll=Roll(
                        groove=ConstrictedBoxGroove(
                            r1=1.81e-3,
                            r2=5.49e-3,
                            r4=12.64e-3,
                            depth=4.65e-3,
                            indent=1e-3,
                            usable_width=25.41e-3,
                            ground_width=17.5e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=4e-3,
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
