from ..universal_elongation import UniversalElongationGroove


class DiamondGrooveBase(UniversalElongationGroove):
    """Base class for diamond like grooves.
    Does not provide any additional functionality to GrooveBase, but can be used as marker class."""

    @property
    def types(self):
        return "diamond",
