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

        super().__init__(usable_width=usable_width)

    @property
    def types(self) -> '("flat",)':
        return "flat",
