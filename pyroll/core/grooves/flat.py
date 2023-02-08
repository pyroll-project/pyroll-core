import numpy as np

from .generic_elongation import GenericElongationGroove


class FlatGroove(GenericElongationGroove):
    """Represents a flat groove aka no groove."""

    def __init__(
            self,
            usable_width: float,
    ):
        """
        :param usable_width: usable width of the roll face
        :type width: float
        """

        super().__init__(usable_width=usable_width, r1=0, r2=0, depth=0, flank_angle=np.pi / 2)

    @property
    def types(self) -> '("flat",)':
        return "flat",
