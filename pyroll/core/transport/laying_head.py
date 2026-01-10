from typing import List, cast
from numpy.typing import NDArray
from ..hooks import Hook
from .transport import Transport

__all__ = ["LayingHead"]


class LayingHead(Transport):
    """Represents a laying with stelmor conveyor belt."""

    winding_diameter = Hook[float]()
    """Diameter of the resulting winding."""

    number_of_windings = Hook[int]()
    """Number of windings."""

    laying_head_velocity = Hook[float]()
    """Velocity of the laying head."""

    stelmor_conveyor_velocity = Hook[float]()
    """Stelmor conveyor velocity."""

    stelmor_layer_distribution = Hook[NDArray]()
    """Distribution of the layer on the stelmor conveyor as numpy array (np.array([[x1, y1]]))."""

    characteristic_layer_section_length = Hook[float]()
    """Length characteristic section of the the wire distribution on the conveyor belt."""

    layer_height = Hook[float]()
    """Height of the layer on the conveyor belt."""

    layer_packing_height = Hook[float]()
    """Height of the layer packing on the conveyor belt."""

    layer_mass_distribution = Hook[NDArray]()
    """Layer mass distribution across the width of the conveyer belt."""

    layer_horizontal_distance = Hook[float]()


    layer_vertical_distance = Hook[float]()
    """Vertical distance of the layer on the conveyor belt."""

    void_ratio = Hook[float]()
    """Void ratio inside the different layers."""

    wire_length_in_characteristic_layer_section_length = Hook[float]()
    """Length of the wire length of the characteristic layer on the conveyor belt."""

    @property
    def disk_elements(self) -> List["LayingHead.DiskElement"]:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def laying_head(self) -> "LayingHead":
            """Reference to the transport. Alias for ``self.unit``."""
            return cast(LayingHead, self.unit)

    class InProfile(Profile, Transport.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, Transport.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def laying_head(self) -> "LayingHead":
            """Reference to the transport. Alias for ``self.parent``."""
            return cast(LayingHead, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> "LayingHead.DiskElement":
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(LayingHead.DiskElement, self.unit)

            @property
            def laying_head(self) -> "LayingHead":
                """Reference to the transport. Alias for ``self.unit.parent``"""
                return cast(LayingHead, self.unit.parent)

        class InProfile(Profile, Transport.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Transport.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
