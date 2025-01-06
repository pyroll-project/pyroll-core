import shapely
import pyroll.core  # noqa


def test_plot_line_string_matplotlib(tmp_path):
    geom = shapely.LineString([(0, 0), (1, 1)])
    p = geom.plot_matplotlib()
    p.savefig(tmp_path / "plot.png")


def test_plot_multi_line_string_matplotlib(tmp_path):
    geom = shapely.MultiLineString([[(0, 0), (1, 1)], [(1, 0), (2, 1)]])
    p = geom.plot_matplotlib()
    p.savefig(tmp_path / "plot.png")


def test_plot_polygon_matplotlib(tmp_path):
    geom = shapely.Polygon([(0, 0), (1, 1), (2, 0)])
    p = geom.plot_matplotlib()
    p.savefig(tmp_path / "plot.png")


def test_plot_multi_polygon_matplotlib(tmp_path):
    geom = shapely.MultiPolygon(
        [
            shapely.Polygon([(0, 0), (1, 1), (2, 0)]),
            shapely.Polygon([(0, 2), (1, 1), (2, 2)]),
        ]
    )
    p = geom.plot_matplotlib()
    p.savefig(tmp_path / "plot.png")


def test_plot_line_string_plotly(tmp_path):
    geom = shapely.LineString([(0, 0), (1, 1)])
    geom.plot_plotly().write_html(tmp_path / "plot.html")


def test_plot_multi_line_string_plotly(tmp_path):
    geom = shapely.MultiLineString([[(0, 0), (1, 1)], [(1, 0), (2, 1)]])
    geom.plot_plotly().write_html(tmp_path / "plot.html")


def test_plot_polygon_plotly(tmp_path):
    geom = shapely.Polygon([(0, 0), (1, 1), (2, 0)])
    geom.plot_plotly().write_html(tmp_path / "plot.html")


def test_plot_multi_polygon_plotly(tmp_path):
    geom = shapely.MultiPolygon(
        [
            shapely.Polygon([(0, 0), (1, 1), (2, 0)]),
            shapely.Polygon([(0, 2), (1, 1), (2, 2)]),
        ]
    )
    geom.plot_plotly().write_html(tmp_path / "plot.html")
