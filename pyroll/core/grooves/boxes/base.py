from ..universal_elongation import UniversalElongationGroove


class BoxGrooveBase(UniversalElongationGroove):
    """Base class for box like grooves.
    Does not provide any additional functionality to GrooveBase, but can be used as marker class."""

    @property
    def types(self):
        return "box",
