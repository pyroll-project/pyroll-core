from .base import GrooveBase

from .spline import SplineGroove
from .generic_elongation import GenericElongationGroove

from .boxes import BoxGroove, ConstrictedBoxGroove, UpsetBoxGroove, ConstrictedUpsetBoxGroove

from .diamonds import DiamondGroove, SquareGroove, GothicGroove

from .ovals import (
    CircularOvalGroove,
    FlatOvalGroove,
    SwedishOvalGroove,
    ConstrictedSwedishOvalGroove,
    Oval3RadiiGroove,
    Oval3RadiiFlankedGroove,
    UpsetOvalGroove,
    ConstrictedCircularOvalGroove
)

from .rounds import RoundGroove, FalseRoundGroove

from .flat import FlatGroove

from .hexagonal import HexagonalGroove

from .equivalent_ripped_groove import EquivalentRibbedGroove

def create_groove_by_type_name(type_name: str, **kwargs) -> GrooveBase:
    """
    Helper function to create a groove instance by giving a type name and respective keyword arguments.
    Supports all grooves from the ``pyroll.core.grooves`` namespace as well as from all currently loaded modules.
    The former take precedence.

    :param type_name: the name of the groove-type either exactly as the respective class name or with words
                      separated by spaces, dashes or underscores where the word capitalization is ignored
    :param kwargs: keyword arguments for constructing the respective groove,
                   allowed arguments depend on the actual groove-type
    """
    import re
    type_name = re.sub(r"[\s\-_.]+(\w)", lambda m: m.group(1).capitalize(), type_name.title())
    type_name = type_name if type_name.endswith("Groove") else type_name + "Groove"

    import sys

    groove_cls = getattr(sys.modules[__name__], type_name, None) # try to get classes of grooves package first

    # otherwise scan over all loaded modules
    if not groove_cls:
        for mod in reversed(sys.modules.values()):
            groove_cls = getattr(mod, type_name, None)

            if groove_cls:
                break

    if not groove_cls:
        raise ValueError(f"No groove class named {type_name} found in loaded modules.")

    return groove_cls(**kwargs)

