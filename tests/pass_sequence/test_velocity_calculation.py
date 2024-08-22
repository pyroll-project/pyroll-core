import logging
import webbrowser

import numpy as np

from pathlib import Path

from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence


# noinspection DuplicatedCode
def test_pass_sequence_velocity_calculation(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        flow_stress=100e6,
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
            ),
            gap=2e-3,

        ),
        Transport(
            label="I => II",
            length=1,
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
            ),
            gap=2e-3,
        ),
        Transport(
            label="II => III",
            length=1
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
            ),
            gap=2e-3,
        ),
    ])

    try:
        sequence.solve_velocities(in_profile=in_profile,
                                  final_speed=1.5,
                                  final_cross_section=sequence[-1].usable_cross_section.area)
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


    velocities = [rp.velocity for rp in sequence.roll_passes]
    assert np.isclose(velocities, [ 0.96401, 964.01e-03]).all
