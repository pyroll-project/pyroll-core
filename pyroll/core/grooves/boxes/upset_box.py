from .box import BoxGroove
from .constricted_box import ConstrictedBoxGroove


class UpsetBoxGroove(BoxGroove):
    """Represents a box-shaped groove with a high height/width ratio."""

    @property
    def types(self) -> '("box", "constricted_box")':
        return "box", "upset"


class ConstrictedUpsetBoxGroove(ConstrictedBoxGroove, UpsetBoxGroove):
    """Represents a box-shaped groove with a high height/width ratio and an indented ground."""

    @property
    def types(self) -> '("box", "constricted_box")':
        return "box", "constricted", "upset"
