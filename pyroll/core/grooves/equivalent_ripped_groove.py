from typing import Optional

import numpy as np

from .generic_elongation import GenericElongationGroove
from .generic_elongation_solvers import solve_r124


class EquivalentRibbedGroove(GenericElongationGroove):
    """Represents a round-shaped groove approximating a ribbed groove using the same mean cross-section area."""

    def __init__(
            self,
            r1: float,
            r3: float,
            rib_distance: float,
            rib_width: float,
            rib_angle: float,
            base_body_height: float,
            nominal_outer_diameter: float,

            pad_angle: float = 0,
            **kwargs
    ):
        """
        All angles are measured in ° (degree).
        Give exactly two of ``r2``, ``depth`` or ``usable_width``.
        Give exactly one of ``flank_angle``, ``flank_width``, ``flank_height`` or ``flank_length``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width

        :param flank_angle: inclination angle of the flanks
        :param flank_width: horizontal extent of the flanks
        :param flank_height: vertical extent of the flanks
        :param flank_length: length of the flanks
        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        """
        pad_angle = np.deg2rad(pad_angle)

        if rib_angle is not None:
            rib_angle = np.deg2rad(rib_angle)

        vertical_rib_width = rib_width / np.cos(rib_angle)
        width_distance_ratio = vertical_rib_width / rib_distance
        nominal_outer_radius = nominal_outer_diameter / 2
        ribbed_circle_segment_height = nominal_outer_radius - base_body_height / 2
        equivalent_circle_segment_height = ribbed_circle_segment_height * width_distance_ratio

        r2 = (4 * equivalent_circle_segment_height ** 2 + base_body_height ** 2) / (
                    8 * equivalent_circle_segment_height)
        alpha = np.deg2rad(45)
        depth = 0
        width = 0


        super().__init__(
            r2=r2, depth=depth, usable_width=width, flank_angle=alpha,
            r1=r1, pad_angle=pad_angle,
            **kwargs
        )

    @property
    def classifiers(self):
        return {"round", "false_round"} | super().classifiers
