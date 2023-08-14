from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np
from shapely.geometry import Polygon, LineString

from ..repr import ReprMixin


class GrooveBase(ReprMixin):
    """Abstract base class for all grooves."""

    @property
    @abstractmethod
    def classifiers(self) -> set[str]:
        """A tuple of keywords to specify the type classifiers of this groove."""
        raise NotImplemented

    @property
    @abstractmethod
    def cross_section(self) -> Polygon:
        """A polygon representing the cross-section of this groove limited by the contour line and y=0."""
        raise NotImplemented

    @property
    @abstractmethod
    def usable_width(self) -> float:
        """The usable width of the groove, meaning the width of ideal filling."""
        raise NotImplemented

    @property
    @abstractmethod
    def width(self) -> float:
        """The maximum width of the groove representing the definition region in z-direction."""
        raise NotImplemented

    @property
    @abstractmethod
    def depth(self) -> float:
        """The maximum depth of the groove."""
        raise NotImplemented

    @property
    @abstractmethod
    def contour_line(self) -> LineString:
        """A line representing the geometry of the groove contour."""
        raise NotImplemented

    @property
    @abstractmethod
    def contour_points(self) -> np.ndarray:
        """An array of the contour line's points of shape (n, 2)."""
        raise NotImplemented

    @abstractmethod
    def local_depth(self, z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Function of the local groove depth in dependence on the z-coordinate."""
        raise NotImplemented

    @property
    def __attrs__(self):
        return {
            n: v for n in ["depth", "usable_width", "classifiers", "contour_line"]
            if (v := getattr(self, n))
        }

    def plot(self, **kwargs):
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            raise RuntimeError(
                "This method is only available if matplotlib is installed in the environment. "
                "You may install it using the 'plot' extra of pyroll-core."
            ) from e

        fig: plt.Figure = plt.figure(**kwargs)
        ax: plt.Axes = fig.subplots()

        ax.set_ylabel("y")
        ax.set_xlabel("z")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        ax.plot(*self.contour_line.xy, color="k")
        return fig
