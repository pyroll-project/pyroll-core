from typing import Optional

import numpy as np

from .generic_elongation import GenericElongationGroove
from .generic_elongation_solvers import solve_r123


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
            usable_width: float,
            depth: float,
            rib_flank_angle: Optional[float] = None,

            pad_angle: float = 0,
            **kwargs
    ):
        """
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r3: radius 3 (ground)
        :param rib_distance: distance between two similar points on two consecutive ribs along the length of the rolled stock
        :param rib_width: rib width
        :param rib_angle: angle between the ribs and an axis along the length of the rolled stock
        :param base_body_height: distance between two parallel faces of the rolled stocks base body
        :param nominal_outer_diameter: the maximum outer diameter
        :param usable_width: usable width
        :param depth: maximum depth


        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        """

        self.nominal_outer_diameter = nominal_outer_diameter
        self.base_body_height = base_body_height
        self.rib_distance = rib_distance
        self.rib_width = rib_width
        self.rib_flank_angle = rib_flank_angle


        pad_angle = np.deg2rad(pad_angle)
        rib_angle = np.deg2rad(rib_angle)

        # Calculation of the radius 2, that makes the equivalent ribbed grove have the same average cross-section,
        # as the non approximated
        vertical_rib_width = rib_width / np.cos(rib_angle)
        width_distance_ratio = vertical_rib_width / rib_distance
        nominal_outer_radius = nominal_outer_diameter / 2
        ribbed_circle_segment_height = nominal_outer_radius - base_body_height / 2
        equivalent_circle_segment_height = ribbed_circle_segment_height * width_distance_ratio

        base_body_diagonal_width = base_body_height * np.sqrt(2)
        help_triangle_inner_angle = np.pi - (np.pi / 4 + (np.pi - np.arcsin(((base_body_diagonal_width / 2) *
                                    np.sin(np.pi / 4)) / nominal_outer_radius)))
        circle_segment_base_width = base_body_height - (2 * ((nominal_outer_radius *
                                    np.sin(help_triangle_inner_angle)) / np.sin(np.pi / 4)))
        r2 = (4 * equivalent_circle_segment_height ** 2 + circle_segment_base_width ** 2) / (
            8 * equivalent_circle_segment_height)

        sol = solve_r123(r1=r1, r2=r2, r3=r3, depth=depth, width=usable_width, pad_angle=pad_angle)

        super().__init__(
            r2=r2, depth=depth, usable_width=usable_width, r1=r1, pad_angle=pad_angle, r3=r3,
            alpha3=sol["alpha3"], flank_angle=sol["flank_angle"],
            **kwargs
        )

    @property
    def classifiers(self):
        return {"equivalent_ribbed", "round", "ribbed"} | super().classifiers
