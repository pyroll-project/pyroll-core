import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pytest
from shapely.geometry import Polygon

import pyroll.core as pr


@pytest.fixture(scope="module")
def main_fig():
    fig = make_subplots(rows=3, cols=5)
    yield fig
    fig.update_layout(title="Contact Areas for Different Profiles")
    fig.show()


@pytest.fixture(scope="module", autouse=True)
def subplot_index():
    index = {"count": 0}
    yield index


ips = {
    "round": pr.Profile.round(
        diameter=30e-3, temperature=1200 + 273.15, material=["C45", "Steel"], length=1, flow_stress=100e6
    ),
    "square": pr.Profile.square(
        side=30e-3, temperature=1200 + 273.15, material=["C45", "Steel"], length=1, flow_stress=100e6
    ),
    "hexagon": pr.Profile.hexagon(
        height=30e-3, temperature=1200 + 273.15, material=["C45", "Steel"], length=1, flow_stress=100e6
    ),
    "box": pr.Profile.box(
        height=30e-3, width=30e-3, temperature=1200 + 273.15, material=["C45", "Steel"], length=1, flow_stress=100e6
    ),
    "diamond": pr.Profile.diamond(
        height=30e-3, width=50e-3, temperature=1200 + 273.15, material=["C45", "Steel"], length=1, flow_stress=100e6
    ),
    "oval": pr.Profile.from_groove(
        pr.CircularOvalGroove(r1=1e-3, depth=12e-3, usable_width=45e-3),
        filling=1,
        height=26e-3,
        flow_stress=100e6,
        material=["C45", "Steel"],
    ),
}

gs = {
    "flat": pr.FlatGroove(usable_width=40e-3),
    "oval": pr.CircularOvalGroove(r1=1e-3, depth=10e-3, usable_width=40e-3),
    "square": pr.SquareGroove(r1=1e-3, r2=5e-3, tip_angle=90, tip_depth=15e-3),
    "round": pr.RoundGroove(r1=1e-3, depth=15e-3, usable_width=31e-3),
}

combinations = [
    (gs["flat"], ips["round"]),
    (gs["flat"], ips["square"]),
    (gs["flat"], ips["hexagon"]),
    (gs["flat"], ips["box"]),
    (gs["flat"], ips["diamond"]),
    (gs["oval"], ips["round"]),
    (gs["oval"], ips["square"]),
    (gs["oval"], ips["hexagon"]),
    (gs["oval"], ips["box"]),
    (gs["square"], ips["diamond"]),
    (gs["square"], ips["oval"]),
    (gs["round"], ips["square"]),
    (gs["round"], ips["diamond"]),
    (gs["round"], ips["oval"]),
]


@pytest.mark.parametrize("g, ip", combinations)
def test_plot_contact_areas_two_rolls(g, ip, main_fig, subplot_index):
    gap = 2e-3
    if "flat" in g.classifiers:
        gap = 20e-3

    rp = pr.RollPass(
        label="test",
        roll=pr.Roll(
            groove=g,
            nominal_radius=150e-3,
            rotational_frequency=1,
        ),
        gap=gap,
    )

    rp.solve(ip)

    fig = rp.plot()

    ca = contact_area(rp)
    x_coords, y_coords = ca.exterior.xy

    x_coords = list(x_coords)
    y_coords = list(y_coords)

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="lines",
            fill="toself",
            line=dict(color="green"),
            fillcolor="rgba(0, 255, 0, 0.3)",
            name="Contact Area",
        )
    )

    idx = subplot_index["count"]
    row = (idx // 5) + 1
    col = (idx % 5) + 1

    subplot_index["count"] += 1

    for trace in fig.data:
        main_fig.add_trace(trace, row=row, col=col)

    roll_contact_area = rp.roll.contact_area

    assert np.isclose(roll_contact_area, ca.area, rtol=1e-3)


def contact_area(rp):
    x1 = -rp.out_profile.width / 2
    x2 = rp.out_profile.width / 2
    x3 = rp.in_profile.width / 2
    x4 = -rp.in_profile.width / 2
    y1 = -rp.roll.contact_length / 2
    y2 = -rp.roll.contact_length / 2
    y3 = rp.roll.contact_length / 2
    y4 = rp.roll.contact_length / 2

    coordinates = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)]
    return Polygon(coordinates)
