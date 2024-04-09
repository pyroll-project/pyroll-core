import logging

import numpy as np
import pytest
from shapely.affinity import rotate

from pyroll.core import SquareGroove, Profile, Config

groove = SquareGroove(0, 3, tip_depth=20, tip_angle=91)


def test_from_groove():
    Profile.from_groove(groove, width=40, height=50)
    Profile.from_groove(groove, filling=0.9, gap=3)


def test_from_groove_errors():
    with pytest.raises(TypeError):
        Profile.from_groove(groove, width=55, filling=0.9, height=50, gap=3)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, width=55, height=50, gap=3)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, width=55, filling=0.9, height=50)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, height=50)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, gap=3)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, width=55)
    with pytest.raises(TypeError):
        Profile.from_groove(groove, filling=0.9)
    with pytest.raises(ValueError):
        Profile.from_groove(groove, height=-1, width=50)
    with pytest.raises(ValueError):
        Profile.from_groove(groove, gap=-1, width=50)
    with pytest.raises(ValueError):
        Profile.from_groove(groove, width=-1, height=50)
    with pytest.raises(ValueError):
        Profile.from_groove(groove, filling=0, height=50)
    with pytest.raises(ValueError):
        Profile.from_groove(groove, width=100, height=50)


def test_from_groove_warnings(caplog):
    logging.getLogger("pyroll").error("Marker Error")

    Profile.from_groove(groove, width=45, height=50)
    Profile.from_groove(groove, filling=1.05, gap=3)

    assert len([r for r in caplog.records if r.levelname == "WARNING" and r.msg.startswith("Encountered")]) > 1


def test_round():
    p1 = Profile.round(radius=15)
    p2 = Profile.round(diameter=30)

    assert p1.cross_section == p2.cross_section


def test_round_errors():
    with pytest.raises(ValueError):
        Profile.round(radius=-1)
    with pytest.raises(ValueError):
        Profile.round(diameter=0)


def test_square():
    p1 = Profile.square(side=10, corner_radius=1)
    p2 = Profile.square(diagonal=10 * np.sqrt(2), corner_radius=1)

    assert p1.cross_section == p2.cross_section

    p3 = Profile.square(side=10)
    p4 = Profile.square(diagonal=10 * np.sqrt(2))

    assert p3.cross_section == p4.cross_section


def test_square_errors():
    with pytest.raises(TypeError):
        Profile.square(side=10, diagonal=10)
    with pytest.raises(TypeError):
        Profile.square()
    with pytest.raises(ValueError):
        Profile.square(side=-1)
    with pytest.raises(ValueError):
        Profile.square(diagonal=0)
    with pytest.raises(ValueError):
        Profile.square(corner_radius=-1, side=10)


def test_box():
    Profile.box(height=10, width=20)
    Profile.box(height=10, width=20, corner_radius=1)


def test_box_errors():
    with pytest.raises(ValueError):
        Profile.box(height=-1, width=5)
    with pytest.raises(ValueError):
        Profile.box(height=10, width=-1)
    with pytest.raises(ValueError):
        Profile.box(corner_radius=-1, height=10, width=5)


def test_diamond():
    Profile.diamond(height=10, width=20)
    Profile.diamond(height=10, width=20, corner_radius=1)


def test_diamond_errors():
    with pytest.raises(ValueError):
        Profile.diamond(height=-1, width=5)
    with pytest.raises(ValueError):
        Profile.diamond(height=10, width=-1)
    with pytest.raises(ValueError):
        Profile.diamond(corner_radius=-1, height=10, width=5)


def test_square_box_equivalence():
    p1 = Profile.square(side=10, corner_radius=0)
    p2 = Profile.box(height=10, width=10, corner_radius=0)
    assert np.isclose(p1.cross_section.symmetric_difference(rotate(p2.cross_section, angle=45, origin=(0, 0))).area, 0)

    p1 = Profile.square(side=10, corner_radius=2)
    p2 = Profile.box(height=10, width=10, corner_radius=2)
    assert np.isclose(p1.cross_section.symmetric_difference(rotate(p2.cross_section, angle=45, origin=(0, 0))).area, 0)


def test_hexagon():
    p1 = Profile.hexagon(side=10)
    p2 = Profile.hexagon(diagonal=20)
    p3 = Profile.hexagon(height=10 * np.sqrt(3))
    assert np.isclose(p1.cross_section.boundary.xy, p2.cross_section.boundary.xy).all()
    assert np.isclose(p1.cross_section.boundary.xy, p3.cross_section.boundary.xy).all()
    Profile.hexagon(side=10, corner_radius=1)


def test_hexagon_errors():
    with pytest.raises(ValueError):
        Profile.hexagon(side=-1)
    with pytest.raises(ValueError):
        Profile.hexagon(diagonal=-1)
    with pytest.raises(ValueError):
        Profile.hexagon(side=10, corner_radius=-1)


def test_refinement(monkeypatch):
    p1 = Profile.square(side=10, corner_radius=1)

    monkeypatch.setattr(Config, "PROFILE_CONTOUR_REFINEMENT", 50)

    p2 = Profile.square(side=10, corner_radius=1)

    import  matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.scatter(*p1.cross_section.boundary.xy, marker="+")
    ax.scatter(*p2.cross_section.boundary.xy, marker="x")
    fig.show()

    assert len(p1.cross_section.boundary.coords) < len(p2.cross_section.boundary.coords)
