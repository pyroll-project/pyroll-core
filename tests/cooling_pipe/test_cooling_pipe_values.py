import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import pi, isclose, rad2deg

from pyroll.core import CoolingPipe, PassSequence, Profile


def test_cooling_pipe_radius():
    cp = CoolingPipe(
        label="Cooling Pipe",
        cross_section_area=10,
    )
    assert np.isclose(cp.inner_radius, 1.784124)


def test_cooling_pipe_area():
    cp = CoolingPipe(
        label="Cooling Pipe",
        inner_radius=1.784124,
    )
    assert np.isclose(cp.cross_section_area, 10)


def test_cooling_pipe_coolant_velocity():
    ip = Profile.round(
        radius=0.5
    )

    seq = PassSequence([
        CoolingPipe(
            label="Cooling Pipe",
            inner_radius=1,
            coolant_volume_flux=1,
            velocity=1,
            length=1
        )])

    seq.solve(ip)

    assert np.isclose(seq[0].coolant_velocity, 0.42418615)


def test_cooling_pipe_coolant_flow_cross_section():
    ip = Profile.round(
        radius=0.5
    )

    seq = PassSequence([
        CoolingPipe(
            label="Cooling Pipe",
            inner_radius=1,
            coolant_volume_flux=1,
            velocity=1,
            length=1
        )])
    seq.solve(ip)

    assert np.isclose(seq[0].coolant_flow_cross_section, 2.357455)
