from ..unit import Unit
from ..hooks import Hook


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

    class Profile(Unit.Profile):
        """Represents a profile in context of a deformation unit."""

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a deformation unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a deformation unit."""
