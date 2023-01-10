import logging
import weakref
from typing import List

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, Polygon

from ..disk_element import DiskedUnit
from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..roll import Roll as BaseRoll
from ..rotator import Rotator


class RollPass(DiskedUnit):
    """Represents a roll pass."""

    in_profile_rotation = Hook[float]()
    """Rotation applied to the incoming profile in ° (degree)."""

    gap = Hook[float]()
    """Gap between the rolls (outer surface)."""

    height = Hook[float]()
    """Maximum height of the roll pass."""

    tip_width = Hook[float]()
    """Width of the intersection of the extended groove flanks (theoretical maximum filling width)."""

    roll_force = Hook[float]()
    """Vertical roll force."""

    mean_flow_stress = Hook[float]()
    """Mean value of the workpiece's flow stress within the pass."""

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

    strain = Hook[float]()
    """Mean equivalent strain applied to the workpiece within the roll pass."""

    strain_rate = Hook[float]()
    """Mean equivalent strain rate within the roll pass."""

    def __init__(
            self,
            roll: BaseRoll,
            label: str = "",
            **kwargs
    ):
        """
        :param roll: the roll object representing the equal working rolls of the pass
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (equal upper and lower)."""

        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    def local_height(self, z: float) -> float:
        coords = np.array([(1, -1), (1, 1)]) * (z, self.height)

        vline = LineString(
            coords
        )

        poly = Polygon(np.concatenate([
            self.upper_contour_line.coords,
            self.lower_contour_line.coords
        ]))

        intersection = vline.intersection(poly)

        return intersection.length

    @property
    def upper_contour_line(self) -> LineString:
        """Contour line object of the upper working roll."""
        return translate(self.roll.contour_line, yoff=self.gap / 2)

    @property
    def lower_contour_line(self) -> LineString:
        """Contour line object of the lower working roll."""
        return rotate(self.upper_contour_line, angle=180, origin=(0, 0))

    @property
    def types(self):
        """A tuple of keywords to specify the shape types of this roll pass.
        Shortcut to ``self.groove.types``."""
        return self.roll.groove.types

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)

        rotator = Rotator(rotation=self.in_profile_rotation, duration=0, length=0)
        rotator.solve(in_profile)

        self.in_profile = self.InProfile(self, rotator.out_profile)
        self.out_profile = self.OutProfile(self, rotator.out_profile)

        self._subunits = self._SubUnitsList(self, [self.DiskElement(self, i) for i in range(self.disk_element_count)])

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    def clear_hook_cache(self):
        super().clear_hook_cache()
        self.roll.clear_hook_cache()

    class Profile(DiskedUnit.Profile):
        """Represents a profile in context of a roll pass."""

        def __init__(self, roll_pass: 'RollPass', template: BaseProfile):
            super().__init__(roll_pass, template)
            self.roll_pass = weakref.ref(roll_pass)

    class InProfile(Profile, DiskedUnit.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, DiskedUnit.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class Roll(BaseRoll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: 'RollPass'):
            kwargs = template.__dict__.copy()
            kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
            super().__init__(**kwargs)
            self.roll_pass = weakref.ref(roll_pass)

    class DiskElement(DiskedUnit.DiskElement):
        """Represents a disk element in a roll pass."""

        contact_area = Hook[float]()
        """Area of contact of the disk element to the rolls."""

        def roll_pass(self) -> 'RollPass':
            return self.parent()
