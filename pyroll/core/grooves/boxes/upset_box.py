from .box import BoxGroove
from .constricted_box import ConstrictedBoxGroove


class UpsetBoxGroove(BoxGroove):
    """Represents a box-shaped groove with a high height/width ratio."""

    @property
    def classifiers(self):
        return {"box", "upset"} | super().classifiers


class ConstrictedUpsetBoxGroove(ConstrictedBoxGroove, UpsetBoxGroove):
    """Represents a box-shaped groove with a high height/width ratio and an indented ground."""

    @property
    def classifiers(self):
        return {"box", "constricted", "upset"} | super().classifiers
