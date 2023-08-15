import matplotlib.pyplot as plt

import pyroll.core as pr


def test_plot_roll_pass_plain():
    p = pr.RollPass(
        roll=pr.Roll(
            groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
        ),
        gap=1
    )

    result = p.plot()

    result.show()


def test_plot_roll_pass_ip():
    p = pr.RollPass(
        roll=pr.Roll(
            groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
        ),
        gap=1
    )
    p.in_profile = pr.Profile.round(diameter=4)

    result = p.plot()

    result.show()


def test_plot_roll_pass_op():
    p = pr.RollPass(
        roll=pr.Roll(
            groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
        ),
        gap=1
    )
    p.out_profile = pr.Profile.square(diagonal=3)

    result = p.plot()

    result.show()
