from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove


class SwedishOvalGroove(GenericElongationGroove):
    """Represents a hexagonal shaped groove that is used like an oval groove (swedish oval)."""

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: float,
            ground_width: Optional[float] = None,
            usable_width: Optional[float] = None,
            flank_angle: Optional[float] = None
    ):
        """
        Exactly two of ground_width, usable_width and flank_angle must be given.

        :param r1: radius of the first edge
        :type r1: float
        :param r2: radius of the second edge
        :type r2: float
        :param depth: depth of the groove
        :type depth: float
        :param ground_width: width of the groove from intersection between two flanks and ground width
        :type ground_width: float
        :param usable_width:  ground width excluding influence of radii
        :type usable_width: float
        :param flank_angle: angle of the flanks
        :type flank_angle: float
        :raises ValueError:  if not exactly two of ground_width, usable_width and flank_angle are given
        """

        if ground_width and usable_width and not flank_angle:
            flank_angle = np.arctan(depth / (usable_width - ground_width) * 2)
        elif usable_width and flank_angle and not ground_width:
            ground_width = usable_width - 2 * depth / np.tan(flank_angle)
        elif ground_width and flank_angle and not usable_width:
            usable_width = ground_width + 2 * depth / np.tan(flank_angle)
        else:
            raise ValueError(
                "Exactly two of the following arguments must be given: ground_width, usable_width, flank_angle."
            )

        even_ground_width = ground_width - 2 * r2 * np.tan(flank_angle / 2)

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=flank_angle, alpha2=flank_angle,
                         even_ground_width=even_ground_width)

    @property
    def types(self) -> '("oval", "swedish_oval")':
        return "oval", "swedish_oval"
