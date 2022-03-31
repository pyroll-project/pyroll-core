from pyroll.core.grooves.universal_elongation import UniversalElongationGroove


class RoundGrooveBase(UniversalElongationGroove):
    """Base class for round like grooves.
    Does not provide any additional functionality to GrooveBase, but can be used as marker class."""

    @property
    def types(self):
        return "round",
