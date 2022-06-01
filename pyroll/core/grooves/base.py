from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np
from shapely.geometry import Polygon, LineString


class GrooveBase(ABC):
    """Abstract base class for all grooves."""

    @property
    @abstractmethod
    def types(self) -> Tuple[str, ...]:
        """A tuple of keywords to specify the types of this groove."""
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
    def depth(self) -> float:
        """The maximum depth of the groove."""
        raise NotImplemented

    @property
    @abstractmethod
    def contour_line(self) -> LineString:
        """A line representing the geometry of the groove contour."""
        raise NotImplemented

    @abstractmethod
    def local_depth(self, z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Function of the local groove depth in dependence on the z-coordinate."""
        raise NotImplemented

    def __str__(self):
        return f"{type(self).__name__} {self.usable_width:.4g} x {self.depth:.4g} ({', '.join(self.types)})"
