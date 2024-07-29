import importlib.util

import pytest
import pyroll.core as pr


@pytest.mark.parametrize(
    "rp",
    [
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1)
            ),
            gap=1,
            in_profile=pr.Profile.round(diameter=4),
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
            gap=1,
            out_profile=pr.Profile.round(diameter=4),
        ),
        pr.RollPass(
            roll=pr.Roll(
                groove=pr.CircularOvalGroove(r1=1, r2=5, depth=1),
                nominal_radius=100
            ),
            gap=1,
            in_profile=pr.Profile.round(diameter=4),
            out_profile=pr.Profile.box(height=3, width=6, corner_radius=1),
        ),
    ]
)
@pytest.mark.xfail(
    not importlib.util.find_spec("matplotlib") and not importlib.util.find_spec("plotly"),
    reason="no plotting backend available"
)
def test_plot_roll_pass_with_profiles_or_not(rp):
    result = rp.plot()
    result.show()


@pytest.mark.parametrize(
    "orientation", [0, 90, "Horizontal", 45, -45, "Vertical"]
)
@pytest.mark.xfail(
    not importlib.util.find_spec("matplotlib") and not importlib.util.find_spec("plotly"),
    reason="no plotting backend available"
)
def test_roll_pass_plot_orientation(orientation):
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


@pytest.mark.parametrize(
    "orientation", [0, 180, "Y", "AntiY", -180]
)
@pytest.mark.xfail(
    not importlib.util.find_spec("matplotlib") and not importlib.util.find_spec("plotly"),
    reason="no plotting backend available"
)
def test_three_roll_pass_plot_orientation(orientation):
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
