import numpy as np
from numpy import deg2rad

from .generic_elongation import GenericElongationGroove


class FlatGroove(GenericElongationGroove):
    """Represents a flat groove aka no groove."""

    def __init__(
            self,
            usable_width: float,
            r1: float = 0,
            pad_angle: float = 0
    ):
        """
        :param usable_width: usable width of the roll face
        """
        pad_angle = deg2rad(pad_angle)

        super().__init__(
            usable_width=usable_width, r1=r1, r2=0, depth=0, flank_angle=0,
            pad_angle=pad_angle,
        )

    @property
    def types(self) -> '("flat",)':
        return "flat",
