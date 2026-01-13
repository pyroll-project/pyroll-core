import numpy as np
from typing import List, cast

from ..hooks import Hook
from .transport import Transport

__all__ = ["Spooler"]


class Spooler(Transport):
    """Represents a spooler for spooled bar in coil."""

    mandrel_radius = Hook[float]()
    """Radius of the mandrel."""

    mandrel_width = Hook[float]()
    """Width of the mandrel."""

    overspeed = Hook[float]()
    """ Percentage of overspeed of the spooler mandrel for hooking."""

    maximum_bending_stress = Hook[float]()
    """Maximum stress to bend a wire."""

    maximum_bending_torque = Hook[float]()
    """Maximum torque to bend a wire."""

    windings_per_layer = Hook[float]()
    """Number of windings per layer."""

    coil_layer_bending_stresses = Hook[np.ndarray]()
    """Bending stress of each layer as a array."""

    coil_layer_bending_torques = Hook[np.ndarray]()
    """Bending torques of each layer as a array."""

    coil_layer_radii = Hook[np.ndarray]()
    """Radii of each layer as a array."""

    coil_layer_torque = Hook[float]()
    """Torque per layer"""

    coil_cumulative_torque = Hook[float]()
    """Total required Torque for all layers"""

    finished_coil_weight = Hook[float]()
    """Finished weight of the resulting coil."""

    finished_coil_radius = Hook[float]()
    """Finished radius of the resulting coil."""

    @property
    def disk_elements(self) -> List["Spooler.DiskElement"]:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def spooler(self) -> "Spooler":
            """Reference to the spooler. Alias for ``self.unit``."""
            return cast(Spooler, self.unit)

    class InProfile(Profile, Transport.InProfile):
        """Represents an incoming profile of a spooler unit."""

    class OutProfile(Profile, Transport.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def spooler(self) -> "Spooler":
            """Reference to the transport. Alias for ``self.parent``."""
            return cast(Spooler, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> "Spooler.DiskElement":
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(Spooler.DiskElement, self.unit)

            @property
            def spooler(self) -> "Spooler":
                """Reference to the transport. Alias for ``self.unit.parent``"""
                return cast(Spooler, self.unit.parent)

        class InProfile(Profile, Transport.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Transport.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
