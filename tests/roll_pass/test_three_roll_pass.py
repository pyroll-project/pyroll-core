import matplotlib.pyplot as plt
import numpy as np
import pytest

from pyroll.core import ThreeRollPass, Roll, CircularOvalGroove, BoxGroove


@pytest.mark.parametrize(
    "g",
    [
        # BoxGroove(
        #     r1=2, r2=3, depth=15, usable_width=40, ground_width=35,
        #     pad_angle=30
        # ),
        # BoxGroove(
        #     r1=4, r2=3, depth=15, usable_width=40, ground_width=35,
        #     pad_angle=30
        # ),
        # BoxGroove(
        #     r1=6, r2=3, depth=15, usable_width=40, ground_width=35,
        #     pad_angle=30
        # ),
        CircularOvalGroove(
            r1=5, r2=40, depth=10,
            pad_angle=30
        ),
        CircularOvalGroove(
            r1=15, r2=40, depth=10,
            pad_angle=30
        ),
        CircularOvalGroove(
            r1=25, r2=40, depth=10,
            pad_angle=30
        )
    ]
)
def test_contour_lines(g):
    rp = ThreeRollPass(
        roll=Roll(
            groove=g
        ),
        gap=2
    )

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.grid()
    plt.plot(*g.contour_line.xy, c="k")
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    plt.xticks(np.linspace(-50, 50, 11))
    plt.yticks(np.linspace(-50, 50, 11))

    for c in rp.contour_lines:
        plt.plot(*c.xy)

    plt.axvline(-rp.gap / 2, c="k", ls="--", lw=1)
    plt.axvline(rp.gap / 2, c="k", ls="--", lw=1)
    plt.axhline(0, c="k", ls="--", lw=1)
    plt.axline((g.z3, g.y3), slope=-np.tan(g.flank_angle), c="k", ls="--", lw=1)

    shift = g.usable_width / 2 / np.sqrt(3) + rp.gap / np.sqrt(3)
    plt.axline((g.z3, -g.y3-shift), slope=np.tan(g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, -g.y1-shift), slope=np.tan(-g.pad_angle), c="r", ls="--", lw=1)

    plt.show()
    plt.close()
