from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np
from shapely.geometry import LineString, Polygon, Point


class GrooveBase(ABC):
    @property
    @abstractmethod
    def types(self) -> Tuple[str]:
        """A tuple of keywords to specify the types of this groove."""
        raise NotImplemented

    @property
    @abstractmethod
    def cross_section(self) -> Polygon:
        """A polygon representing the cross-section of this profile"""
        raise NotImplemented

    @property
    @abstractmethod
    def usable_width(self) -> float:
        raise NotImplemented

    @property
    @abstractmethod
    def depth(self) -> float:
        raise NotImplemented

    @property
    @abstractmethod
    def contour_line(self) -> LineString:
        raise NotImplemented

    @abstractmethod
    def local_depth(self, z) -> Union[float, np.ndarray]:
        raise NotImplemented

    def __str__(self):
        return f"{type(self).__name__} {self.usable_width:.4g} x {self.depth:.4g} ({', '.join(self.types)})"
