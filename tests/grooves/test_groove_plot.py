import importlib.util

import pytest

import pyroll.core as pr


@pytest.mark.xfail(
    not importlib.util.find_spec("matplotlib") and not importlib.util.find_spec("plotly"),
    reason="no plotting backend available",
)
def test_plot_groove():
    groove = pr.CircularOvalGroove(r1=1, r2=5, depth=1)
    result = groove.plot()
    result.show()
