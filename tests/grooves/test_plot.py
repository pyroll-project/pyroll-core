import matplotlib.pyplot as plt

import pyroll.core as pr


def test_plot_groove():
    groove = pr.CircularOvalGroove(r1=1, r2=5, depth=1)

    result = groove.plot()

    result.show()
