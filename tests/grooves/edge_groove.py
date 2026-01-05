import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import PreformingGroove,  Roll, AsymmetricTwoRollPass


def check(g):
    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.grid()
    plt.show()
    plt.close()

def test_upper_edge_groove_visual():
    g = PreformingGroove(r1=30e-3, r2=2e-3, tip_angle=100, usable_width=85e-3, tip_depth=20e-3)
    check(g)

def test_lower_edge_groove_visual():
    g = PreformingGroove(r1=60e-3, r2=40e-3, usable_width=85e-3, tip_depth=5e-3)
    check(g)

def test_precontour_pass():
    upper_groove = PreformingGroove(r1=30e-3, r2=2e-3, tip_angle=100, usable_width=85e-3, tip_depth=20e-3)
    lower_groove = PreformingGroove(r1=60e-3, r2=40e-3, usable_width=85e-3, tip_depth=5e-3)

    rp = AsymmetricTwoRollPass(
        label="Angle Edge Pass",
        upper_roll=Roll(
            groove=upper_groove,
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        lower_roll=Roll(
            groove=lower_groove,
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        lower_groove_rotation=0,
        gap=11e-3,
    )

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    for cl in rp.contour_lines.geoms:
        plt.plot(*cl.xy, color='black')
    plt.grid()
    plt.show()
    plt.close()


# width = 85;
#  tip_angle = 100;
#  tip_radius = 2;
#  trans_radius_top = 30;
#  radius_bottom = 40;
#  trans_radius_bottom = 60;
#  depth_top = 20;
#  depth_bottom = 5;
#  gap_top = 4;
#  gap_bottom = 7;

