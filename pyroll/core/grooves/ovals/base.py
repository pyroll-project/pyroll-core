from ..universal_elongation import UniversalElongationGroove


class OvalGrooveBase(UniversalElongationGroove):
    """Base class for oval like grooves.
    Does not provide any additional functionality to GrooveBase, but can be used as marker class."""

    @property
    def types(self):
        return "oval",
