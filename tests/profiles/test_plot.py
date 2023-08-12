import matplotlib.pyplot as plt

import pyroll.core as pr


def test_plot_profile():
    p = pr.Profile.square(side=10, corner_radius=2)

    result = p.plot()

    result.show()