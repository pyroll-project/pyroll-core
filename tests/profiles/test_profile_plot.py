import importlib.util

import pytest

import pyroll.core as pr


@pytest.mark.parametrize(
    "p", [pr.Profile.square(side=10, corner_radius=2), pr.Profile.hexagon(side=10, corner_radius=2)]
)
@pytest.mark.xfail(
    not importlib.util.find_spec("matplotlib") and not importlib.util.find_spec("plotly"),
    reason="no plotting backend available",
)
def test_plot_profile(p):
    result = p.plot()
    result.show()
