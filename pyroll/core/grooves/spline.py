import numpy as np
import scipy.interpolate
from pathlib import Path
from shapely.geometry import Polygon, LineString
from typing import Union, Tuple, Iterable, Optional

from pyroll.core.grooves import GrooveBase


class SplineGroove(GrooveBase):
    """Represents a groove defined by a linear spline contour."""

    def __init__(
        self,
        contour_points: Union[Iterable[Tuple[float, float]], np.ndarray],
        classifiers: Iterable[str],
        usable_width: Optional[float] = None,
    ):
        """
        :param contour_points: an iterable of contour points to be used for the spline
        :param classifiers: an iterable of string keys used as type classifiers
        :param usable_width: the usable width to assume for this instance, if None, the maximum width will be used
        """
        contour_points = np.asarray(contour_points, dtype="float64")

        if contour_points.ndim != 2:
            raise ValueError("contour_points must be two-dimensional")

        if contour_points.shape[1] != 2:
            raise ValueError("contour_points must have length of 2 in second dimension")

        if not np.isclose(contour_points[0, 1], 0) or not np.isclose(contour_points[-1, 1], 0):
            raise ValueError("first and last element of contour_points should have y coordinate equal to 0")

        # strip boundary
        contour_points = contour_points[
            np.logical_not(
                (np.isclose(np.roll(contour_points[:, 1], 1), 0)) & (np.isclose(np.roll(contour_points[:, 1], -1), 0))
            )
        ]

        # shift center to 0,0
        contour_points[:, 0] -= np.mean(contour_points[:, 0])

        half_width = contour_points[-1, 0]

        if usable_width:
            self._usable_width = usable_width
        else:
            self._usable_width = half_width * 2

        self._contour_points = contour_points
        self._contour_line = LineString(contour_points)
        self._cross_section = Polygon(self._contour_line)
        self._width = half_width * 2

        self._depth = np.max(contour_points[:, 1])

        self._local_depth = scipy.interpolate.interp1d(
            contour_points[:, 0], contour_points[:, 1], fill_value="extrapolate"
        )
        self._classifiers = tuple(classifiers)

    @property
    def classifiers(self) -> Tuple[str, ...]:
        return self._classifiers

    @property
    def cross_section(self) -> Polygon:
        return self._cross_section

    @property
    def usable_width(self) -> float:
        return self._usable_width

    @property
    def width(self) -> float:
        return self._width

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def contour_points(self):
        return self._contour_points

    @property
    def contour_line(self) -> LineString:
        return self._contour_line

    def local_depth(self, z) -> Union[float, np.ndarray]:
        return self._local_depth(z)

    @classmethod
    def from_dxf_drawing(
        cls,
        filepath: Path,
        classifiers: Iterable[str],
        usable_width: Optional[float] = None,
        arc_degrees_per_segment: float = 0.5,
        spline_delta: float = 0.1,
        dxf_query: str = '* [layer=="0"]',
    ) -> "SplineGroove":
        """
        Creates a spline groove with a given contour line as defined inside the .dxf drawing.

        :param filepath: the filepath to the drawing
        :param classifiers: an iterable of string keys used as type classifiers
        :param usable_width: the usable width to assume for this instance, if None, the maximum width will be used
        :param arc_degrees_per_segment: discretization width in degrees for arcs and circles
        :param dxf_query: query to filter the wanted geometries out of the dxf, see the ezdxf docs for details
        """

        try:
            from ezdxf import readfile
            from ezdxf_shapely import convert_all, line_merge
        except ImportError as e:
            raise RuntimeError("ezdxf-shapely is required for DXF import, you may install it with the dxf extra") from e
        from shapely.affinity import translate

        dxf_doc = readfile(filepath)
        msp = dxf_doc.modelspace().query(dxf_query)
        geoms = convert_all(msp, spline_delta=spline_delta, degrees_per_segment=arc_degrees_per_segment)
        geom = line_merge(geoms)
        geom = translate(geom, -geom.centroid.x, -geom.bounds[1])

        return SplineGroove(contour_points=geom.coords, classifiers=classifiers, usable_width=usable_width)
