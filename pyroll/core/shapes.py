import numpy as np

from pyroll.core.repr import ReprMixin
from shapely import Polygon, LineString, MultiPolygon, MultiLineString


@property
def height(self) -> float:
    """Computes the height of the bounding box."""
    return self.bounds[3] - self.bounds[1]


@property
def width(self) -> float:
    """Computes the width of the bounding box."""
    return self.bounds[2] - self.bounds[0]


@property
def perimeter(self) -> float:
    """Get the perimeter of the Polygon (alias of ``Polygon.length``)."""
    return self.length


@property
def polygon_attrs(self):
    return {
        "width": self.width,
        "height": self.height,
        "perimeter": self.perimeter,
        "area": self.area,
    }


@property
def line_string_attrs(self):
    return {
        "width": self.width,
        "height": self.height,
        "length": self.length,
    }


def polygon_plot_matplotlib(self: Polygon):
    import matplotlib.pyplot as plt

    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_ylabel("y")
    ax.set_xlabel("z")

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    ax.plot(*self.boundary.xy, color="k")
    ax.fill(*self.boundary.xy, color="k", alpha=0.5)
    return fig


def polygon_plot_plotly(self: Polygon):
    import plotly.express as px

    fig = px.line(
        x=self.boundary.xy[0],
        y=self.boundary.xy[1],
        labels={"y": "y", "x": "z"},
    )

    fig.update_traces(
        fill="toself"
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1
    )

    return fig


def multi_polygon_plot_matplotlib(self: MultiPolygon):
    import matplotlib.pyplot as plt

    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_ylabel("y")
    ax.set_xlabel("z")

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    for g in self.geoms:
        l = ax.plot(*g.boundary.xy)
        ax.fill(*g.boundary.xy, alpha=0.5, color=l[0].get_color())
    return fig


def multi_polygon_plot_plotly(self: MultiPolygon):
    import plotly.graph_objects as pgo

    fig = pgo.Figure()

    for g in self.geoms:
        fig.add_trace(pgo.Line(
            x=np.array(g.boundary.xy[0]),
            y=np.array(g.boundary.xy[1]),
        ))

    fig.update_traces(
        fill="toself"
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
        title="y"
    )

    fig.update_xaxes(title="z")

    return fig


def line_string_plot_matplotlib(self: LineString):
    import matplotlib.pyplot as plt

    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_ylabel("y")
    ax.set_xlabel("z")

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    ax.plot(*self.xy)
    return fig


def line_string_plot_plotly(self: LineString):
    import plotly.express as px

    fig = px.line(
        x=self.xy[0],
        y=self.xy[1],
        labels={"y": "y", "x": "z"},
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1
    )

    return fig


def multi_line_string_plot_matplotlib(self: MultiLineString):
    import matplotlib.pyplot as plt

    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_ylabel("y")
    ax.set_xlabel("z")

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    for g in self.geoms:
        ax.plot(*g.xy)
    return fig


def multi_line_string_plot_plotly(self: MultiLineString):
    import plotly.graph_objects as pgo

    fig = pgo.Figure()

    for g in self.geoms:
        fig.add_trace(pgo.Line(
            x=np.array(g.xy[0]),
            y=np.array(g.xy[1]),
        ))

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
        title="y"
    )

    fig.update_xaxes(title="z")

    return fig


for cls in [
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
]:
    cls.height = height
    cls.width = width
    cls.__str__ = ReprMixin.__str__
    cls.__repr__ = ReprMixin.__repr__
    # noinspection PyProtectedMember
    cls._repr_html_ = ReprMixin._repr_html_
    # noinspection PyProtectedMember
    cls._repr_pretty_ = ReprMixin._repr_pretty_
    cls.plot = ReprMixin.plot
    cls.plot_matplotlib = ReprMixin.plot_matplotlib
    cls.plot_plotly = ReprMixin.plot_plotly

for cls in [
    Polygon,
    MultiPolygon,
]:
    cls.perimeter = perimeter
    cls.__attrs__ = polygon_attrs

for cls in [
    LineString,
    MultiLineString,
]:
    cls.__attrs__ = line_string_attrs

# noinspection PyProtectedMember
Polygon._plot_matplotlib_ = polygon_plot_matplotlib
# noinspection PyProtectedMember
Polygon._plot_plotly_ = polygon_plot_plotly

# noinspection PyProtectedMember
MultiPolygon._plot_matplotlib_ = multi_polygon_plot_matplotlib
# noinspection PyProtectedMember
MultiPolygon._plot_plotly_ = multi_polygon_plot_plotly

# noinspection PyProtectedMember
LineString._plot_matplotlib_ = line_string_plot_matplotlib
# noinspection PyProtectedMember
LineString._plot_plotly_ = line_string_plot_plotly

# noinspection PyProtectedMember
MultiLineString._plot_matplotlib_ = multi_line_string_plot_matplotlib
# noinspection PyProtectedMember
MultiLineString._plot_plotly_ = multi_line_string_plot_plotly

_RECTANGLE_CORNERS = np.asarray(
    [
        (-0.5, -0.5),
        (0.5, -0.5),
        (0.5, 0.5),
        (-0.5, 0.5)
    ]
)


def rectangle(width: float, height: float):
    """
    Creates an instance of :py:class:`Polygon` with rectangular shape from height and width aligned to the axes.

    :param width: the width of the rectangle
    :param height: the height of the rectangle
    """

    try:
        width = float(width)
        height = float(height)

    except TypeError as e:
        raise TypeError("width and height must be convertible to float") from e

    points = _RECTANGLE_CORNERS * (width, height)
    rect = Polygon(points)

    return rect
