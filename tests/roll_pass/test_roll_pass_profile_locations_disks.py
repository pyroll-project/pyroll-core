import logging
from pathlib import Path

import numpy as np

from pyroll.core import Profile, Roll, RollPass, CircularOvalGroove


# noinspection DuplicatedCode


def test_cartesian_positions(tmp_path: Path, caplog, monkeypatch):
    monkeypatch.setenv("PYROLL_REPORT_PRINT_DISK_ELEMENTS", "True")

    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        length=1,
    )

    rp = RollPass(
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
        disk_element_count=5,
    )

    try:
        rp.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    ip_pos = [de.in_profile.x for de in rp.disk_elements]
    op_pos = [de.out_profile.x for de in rp.disk_elements]
    assert np.isclose(ip_pos, [-0.04228475, -0.0338278, -0.02537085, -0.0169139, -0.00845695]).all()
    assert np.isclose(op_pos, [-0.0338278, -0.02537085, -0.0169139, -0.00845695, 0]).all()


def test_cylindrical_positions(tmp_path: Path, caplog, monkeypatch):
    monkeypatch.setenv("PYROLL_REPORT_PRINT_DISK_ELEMENTS", "True")

    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        length=1,
    )

    rp = RollPass(
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
        disk_element_count=5,
    )

    try:
        rp.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    ip_angle = [de.in_profile.longitudinal_angle for de in rp.disk_elements]
    op_angle = [de.out_profile.longitudinal_angle for de in rp.disk_elements]
    assert np.isclose(ip_angle, [-0.2739, -0.2181, -0.1630, -0.1084, -0.0541], rtol=1e-3).all()
    assert np.isclose(op_angle, [-0.2181, -0.1630, -0.1084, -0.0541, 0], rtol=1e-3).all()
