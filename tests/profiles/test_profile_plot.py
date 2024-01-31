import pytest

import pyroll.core as pr


@pytest.mark.parametrize(
    "p",
    [
        pr.Profile.square(side=10, corner_radius=2),
        pr.Profile.hexagon(side=10, corner_radius=2)
    ]
)
def test_plot_profile(p):
    if pr.PLOTTING_BACKEND is not None:
        result = p.plot()
        result.show()

        if pr.PLOTTING_BACKEND == "matplotlib":
            from matplotlib.pyplot import Figure
            assert isinstance(result, Figure)

        if pr.PLOTTING_BACKEND == "plotly":
            from plotly.graph_objects import Figure
            assert isinstance(result, Figure)
