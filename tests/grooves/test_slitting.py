import matplotlib.pyplot as plt
import numpy as np

from pyroll.core import RoundGroove, SlittingGroove, CircularOvalGroove


def plot(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-50, 50)
    plt.ylim(0, 10)
    plt.show()
    plt.close()


def test_slitting_round():
    g = SlittingGroove(RoundGroove, separator_indent=2, depth=9, r1=2, r2=10, pad_angle=0)
    plot(g)

    assert np.isclose(g.usable_width / 2, 20.97846881)
