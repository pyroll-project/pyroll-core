import matplotlib.pyplot as plt

import pyroll.core as pr


def test_plot_groove():
    if pr.PLOTTING_BACKEND is not None:
        groove = pr.CircularOvalGroove(r1=1, r2=5, depth=1)
        result = groove.plot()
        result.show()

        if pr.PLOTTING_BACKEND == "matplotlib":
            from matplotlib.pyplot import Figure
            assert isinstance(result, Figure)

        if pr.PLOTTING_BACKEND == "plotly":
            from plotly.graph_objects import Figure
            assert isinstance(result, Figure)

