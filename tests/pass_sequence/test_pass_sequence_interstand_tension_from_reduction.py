import logging
import webbrowser

import numpy as np

from pathlib import Path

from pyroll.core import (
    Profile,
    Roll,
    RollPass,
    Transport,
    RoundGroove,
    CircularOvalGroove,
    PassSequence,
    root_hooks,
    Rotator, FalseRoundGroove,
)


def width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    return self.roll_pass.in_profile.width * self.roll_pass.draught ** -0.5


def test_pass_sequence_interstand_calculation_with_reductions(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    with RollPass.OutProfile.width(width):
        root_hooks.add(RollPass.OutProfile.width)
        root_hooks.add(Rotator.OutProfile.width)

        reductions = np.array([1.241, 1.229, 1.276])

        in_profile = Profile.round(
            diameter=17e-3,
            temperature=1200 + 273.15,
            material=["C45", "steel"],
            flow_stress=100e6,
            elastic_modulus=53e6
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Oval I",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=4.35e-3,
                            r1=1.8e-3,
                            r2=18.5e-3
                        ),
                        nominal_radius=208e-3,
                    ),
                    gap=2.05e-3,
                ),
                Transport(
                    label="I => II",
                    length=1,
                ),
                RollPass(
                    label="Round II",
                    roll=Roll(
                        groove=FalseRoundGroove(
                            r1=1.55e-3,
                            r2=7.1e-3,
                            flank_angle=60,
                            depth=6e-3
                        ),
                        nominal_radius=208e-3,
                    ),
                    gap=1.550e-3,
                ),
                Transport(label="II => III", length=1),
                RollPass(
                    label="Oval III",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=3.6e-3,
                            r1=1.4e-3,
                            r2=15e-3
                        ),
                        nominal_radius=208e-3,
                    ),
                    gap=1.4e-3,
                ),
            ]
        )

        try:
            sequence.solve_interstand_tensions_with_given_velocity_ratios(in_profile=in_profile, final_speed=20.47, velocity_ratios=reductions)
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
#
# velocities = [rp.velocity for rp in sequence.roll_passes]
# assert np.isclose(velocities[-1], 1.5).all()
#
# in_profile_velocities = np.zeros_like(sequence.roll_passes)
# for i in range(1, len(sequence.roll_passes)):
#     in_profile_velocities[i] = sequence.roll_passes[i].in_profile.velocity
#
# out_profile_velocities = np.asarray([rp.out_profile.velocity for rp in sequence.roll_passes])
#
# for i in range(1, len(sequence.roll_passes)):
#     assert np.isclose(in_profile_velocities[i], out_profile_velocities[i - 1], atol=1e-3)
