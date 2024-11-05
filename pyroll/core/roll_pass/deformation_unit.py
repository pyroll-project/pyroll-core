import numpy as np

from ..unit import Unit
from ..hooks import Hook
from shapely.geometry import MultiLineString
from typing import List


class DeformationUnit(Unit):
    strain = Hook[float]()
    """Mean equivalent strain applied to the workpiece."""

    strain_rate = Hook[float]()
    """Mean equivalent strain rate."""

    spread = Hook[float]()
    """Coefficient of spread (change in width)."""

    elongation = Hook[float]()
    """Coefficient of elongation (change in length)."""

    draught = Hook[float]()
    """Coefficient of draught (change in height)."""

    log_spread = Hook[float]()
    """Log. coefficient of spread (change in width)."""

    log_elongation = Hook[float]()
    """Log. coefficient of elongation (change in length)."""

    log_draught = Hook[float]()
    """Log. coefficient of draught (change in height)."""

    abs_spread = Hook[float]()
    """Absolute spread (change in width)."""

    abs_elongation = Hook[float]()
    """Absolute elongation (change in length)."""

    abs_draught = Hook[float]()
    """Absolute draught (change in height)."""

    rel_spread = Hook[float]()
    """Relative spread (change in width)."""

    rel_elongation = Hook[float]()
    """Relative elongation (change in length)."""

    rel_draught = Hook[float]()
    """Relative draught (change in height)."""

    contact_area = Hook[float]()
    """Area of contact of the workpiece to the rolls."""

    free_surface_area = Hook[float]()
    """Area of free surface."""

    deformation_resistance = Hook[float]()
    """Equivalent deformation resistance (mean flow stress increased by deformation efficiency)."""

    contact_pressure = Hook[float]()
    """Pressure acting on the contact area."""

    contact_friction = Hook[float]()
    """Friction stress acting on the contact area."""

    zener_holomon_parameter = Hook[float]()
    """Temperature corrected strain rate acc. to Zener and Holomon."""

    class Profile(Unit.Profile):
        """Represents a profile in context of a deformation unit."""

        contact_lines = Hook[MultiLineString]()
        """List of lines that are in contact with tooling (rolls)."""

        contact_angles = Hook[List[np.ndarray]]()
        """List of contour angles that are in contact with tooling (rolls)."""

        free_surface_lines = Hook[MultiLineString]()
        """List of lines that are not in contact with tooling (rolls)."""

        contact_width = Hook[float]()
        """Projected width of contact lines."""

        contact_depth = Hook[float]()
        """Projected depth of contact lines."""

        longitudinal_angle = Hook[float]()
        """Longitudinal angle between the deformation unit and the workpiece."""

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a deformation unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a deformation unit."""
