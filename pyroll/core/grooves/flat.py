from .generic_elongation import GenericElongationGroove


class FlatGroove(GenericElongationGroove):
    """Represents a box shaped groove."""

    def __init__(
            self,
            width: float,
    ):
        """
        :param width: width of the forming zone
        :type width: float
        """

        super().__init__(usable_width=width)

    @property
    def types(self) -> '("flat",)':
        return "flat",
