from typing import Union, Tuple, Iterable, Optional

import numpy as np
import scipy.interpolate
from shapely.geometry import Polygon, LineString

from pyroll.core.grooves import GrooveBase


class SplineGroove(GrooveBase):
    """Represents a groove defined by a linear spline contour."""

    def __init__(self,
                 contour_points: Union[Iterable[Tuple[float, float]], np.ndarray],
                 types: Iterable[str],
                 usable_width: Optional[float] = None,
                 ):
        """
        :param contour_points: an iterable of contour points to be used for the spline
        :param types: an interable of string keys used as type classifiers
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
        contour_points = contour_points[np.logical_not(
            (np.isclose(np.roll(contour_points[:, 1], 1), 0)) & (np.isclose(np.roll(contour_points[:, 1], -1), 0)))]

        # shift center to 0,0
        contour_points[:, 0] -= np.mean(contour_points[:, 0])

        half_width = contour_points[-1, 0]

        if usable_width:
            self._usable_width = usable_width
        else:
            self._usable_width = half_width * 2

        # buffer boundaries
        contour_points = np.insert(contour_points, 0, (-half_width * 1.1, 0), axis=0)
        contour_points = np.append(contour_points, [(half_width * 1.1, 0)], axis=0)

        self._contour_line = LineString(contour_points)
        self._cross_section = Polygon(self._contour_line)

        self._depth = np.max(contour_points[:, 1])

        self._local_depth = scipy.interpolate.interp1d(contour_points[:, 0], contour_points[:, 1],
                                                       fill_value="extrapolate")
        self._types = tuple(types)

    @property
    def types(self) -> Tuple[str, ...]:
        return self._types

    @property
    def cross_section(self) -> Polygon:
        return self._cross_section

    @property
    def usable_width(self) -> float:
        return self._usable_width

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def contour_line(self) -> LineString:
        return self._contour_line

    def local_depth(self, z) -> Union[float, np.ndarray]:
        return self._local_depth(z)
