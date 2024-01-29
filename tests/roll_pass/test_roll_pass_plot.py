import matplotlib.pyplot as plt
import pytest

import pyroll.core as pr


@pytest.mark.parametrize(
    "rp",
    [
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
            ),
            gap=1
        ),
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
            ),
            gap=1
        ),
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
            ),
            gap=1
        ),
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1),
                nominal_radius=100
            ),
            gap=1,
            rotation=0,
            velocity=1,
        ),
    ]
)
def test_plot_roll_pass_with_profiles_or_not(rp):
    if pr.PLOTTING_BACKEND is not None:
        result = rp.plot()
        result.show()

        if pr.PLOTTING_BACKEND == "matplotlib":
            from matplotlib.pyplot import Figure
            assert isinstance(result, Figure)

        if pr.PLOTTING_BACKEND == "plotly":
            from plotly.graph_objects import Figure
            assert isinstance(result, Figure)


@pytest.mark.parametrize(
    "orientation", [0, 90, "Horizontal", 45, -45, "Vertical"]
)
def test_roll_pass_plot_orientation(orientation):
    if pr.PLOTTING_BACKEND is not None:
        rp = pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1),
                nominal_radius=100
            ),
            gap=1,
            orientation=orientation,
            rotation=0,
            velocity=1,
        )
        rp.solve(pr.Profile.box(height=6, width=4, flow_stress=100e6))
        result = rp.plot()
        result.show()

        if pr.PLOTTING_BACKEND == "matplotlib":
            from matplotlib.pyplot import Figure
            assert isinstance(result, Figure)

        if pr.PLOTTING_BACKEND == "plotly":
            from plotly.graph_objects import Figure
            assert isinstance(result, Figure)


@pytest.mark.parametrize(
    "orientation", [0, 180, "Y", "AntiY", -180]
)
def test_three_roll_pass_plot_orientation(orientation):
    if pr.PLOTTING_BACKEND is not None:
        rp = pr.ThreeRollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1, pad_angle=30),
                nominal_radius=100,
            ),
            gap=1,
            orientation=orientation,
            rotation=0,
            velocity=1,
        )
        rp.solve(pr.Profile.round(diameter=7.5, flow_stress=100e6))
        result = rp.plot()
        result.show()

        if pr.PLOTTING_BACKEND == "matplotlib":
            from matplotlib.pyplot import Figure
            assert isinstance(result, Figure)

        if pr.PLOTTING_BACKEND == "plotly":
            from plotly.graph_objects import Figure
            assert isinstance(result, Figure)

