from abc import abstractmethod
from typing import Union

import numpy as np
from shapely.geometry import Polygon, LineString

from ..repr import ReprMixin

__all__ = ["GrooveBase"]


class GrooveBase(ReprMixin):
    """Abstract base class for all grooves."""

    @property
    @abstractmethod
    def classifiers(self) -> set[str]:
        """A tuple of keywords to specify the type classifiers of this groove."""
        raise NotImplementedError

    @property
    @abstractmethod
    def cross_section(self) -> Polygon:
        """A polygon representing the cross-section of this groove limited by the contour line and y=0."""
        raise NotImplementedError

    @property
    @abstractmethod
    def usable_width(self) -> float:
        """The usable width of the groove, meaning the width of ideal filling."""
        raise NotImplementedError

    @property
    @abstractmethod
    def width(self) -> float:
        """The maximum width of the groove representing the definition region in z-direction."""
        raise NotImplementedError

    @property
    @abstractmethod
    def depth(self) -> float:
        """The maximum depth of the groove."""
        raise NotImplementedError

    @property
    @abstractmethod
    def contour_line(self) -> LineString:
        """A line representing the geometry of the groove contour."""
        raise NotImplementedError

    @property
    @abstractmethod
    def groove_factor(self) -> LineString:
        """The groove factor marks the y - position of the working radius ."""
        raise NotImplementedError

    @property
    @abstractmethod
    def contour_points(self) -> np.ndarray:
        """An array of the contour line's points of shape (n, 2)."""
        raise NotImplementedError

    @abstractmethod
    def local_depth(self, z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Function of the local groove depth in dependence on the z-coordinate."""
        raise NotImplementedError

    @property
    def __attrs__(self):
        return {n: v for n in ["depth", "usable_width", "classifiers", "contour_line"] if (v := getattr(self, n))}

    def _plot_matplotlib_(self):
        import matplotlib.pyplot as plt

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()

        ax.set_ylabel("y")
        ax.set_xlabel("z")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        ax.plot(*self.contour_line.xy, color="k")
        return fig

    def _plot_plotly_(self):
        import plotly.express as px

        fig = px.line(
            x=self.contour_line.xy[0],
            y=self.contour_line.xy[1],
            labels={"y": "y", "x": "z"},
        )

        fig.update_traces(line_color="black")

        fig.update_yaxes(scaleanchor="x", scaleratio=1)

        return fig
