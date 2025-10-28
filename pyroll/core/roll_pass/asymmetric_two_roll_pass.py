from typing import List, cast
from shapely.affinity import translate, scale
from shapely.geometry.multilinestring import MultiLineString

import weakref
import numpy as np

from .base import BaseRollPass
from ..hooks import Hook
from ..roll import Roll as BaseRoll
from ..engine import Engine as BaseEngine

class AsymmetricTwoRollPass(BaseRollPass):
    """Represents a symmetric roll pass with unequal upper and lower roll."""

    def __init__(
            self,
            upper_roll: BaseRoll,
            lower_roll: BaseRoll,
            engine: BaseEngine = BaseEngine(),
            label: str = "",
            **kwargs
    ):
        super().__init__(label, **kwargs)

        self.upper_roll = self.UpperRoll(upper_roll, self)
        """The upper roll of this pass."""

        self.lower_roll = self.LowerRoll(lower_roll, self)
        """The lower roll of this pass."""

        self.engine = self.Engine(engine, self)
        """The engine of this pass."""

    @property
    def contour_lines(self) -> MultiLineString:
        if self._contour_lines:
            return self._contour_lines

        upper = translate(self.upper_roll.contour_line, yoff=self.gap / 2)
        lower = scale(
            translate(self.lower_roll.contour_line.reverse(), yoff=self.gap / 2),
            xfact=1, yfact=-1, origin=(0, 0)
        )

        self._contour_lines = MultiLineString([upper, lower])
        return self._contour_lines

    @property
    def classifiers(self):
        """A tuple of keywords to specify the shape type classifiers of this roll pass.
        Shortcut to ``self.groove.classifiers``."""
        return set(self.upper_roll.groove.classifiers) | set(self.lower_roll.groove.classifiers) | {"asymmetric"}

    @property
    def disk_elements(self) -> List['AsymmetricTwoRollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        upper_roll_results = self.upper_roll.evaluate_and_set_hooks()
        lower_roll_results = self.lower_roll.evaluate_and_set_hooks()
        return np.concatenate([super_results, upper_roll_results, lower_roll_results], axis=0)

    def reevaluate_cache(self):
        super().reevaluate_cache()
        self.upper_roll.reevaluate_cache()
        self.lower_roll.reevaluate_cache()
        self._contour_lines = None

    class Profile(BaseRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'AsymmetricTwoRollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(AsymmetricTwoRollPass, self.unit)

    class InProfile(Profile, BaseRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

        pass_line = Hook[tuple[float, float, float]]()
        """Point (x, y, z) where the incoming profile centroid enters the roll pass."""

    class OutProfile(Profile, BaseRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class UpperRoll(BaseRoll):
        """Represents the upper roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: "AsymmetricTwoRollPass"):
            kwargs = dict(e for e in template.__dict__.items() if not e[0].startswith("_"))
            super().__init__(**kwargs)

            self._roll_pass = weakref.ref(roll_pass)

        entry_angle = Hook[float]()
        """Angle at which the material enters the roll gap."""

        exit_angle = Hook[float]()
        """Angle at which the material exits the roll gap."""

        @property
        def roll_pass(self):
            """Reference to the roll pass this roll is used in."""
            return self._roll_pass()

    class LowerRoll(BaseRoll):
        """Represents the lower roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: "AsymmetricTwoRollPass"):
            kwargs = dict(e for e in template.__dict__.items() if not e[0].startswith("_"))
            super().__init__(**kwargs)

            self._roll_pass = weakref.ref(roll_pass)

        entry_angle = Hook[float]()
        """Angle at which the material enters the roll gap."""

        exit_angle = Hook[float]()
        """Angle at which the material exits the roll gap."""

        @property
        def roll_pass(self):
            """Reference to the roll pass this roll is used in."""
            return self._roll_pass()

    class DiskElement(BaseRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'AsymmetricTwoRollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(AsymmetricTwoRollPass, self.parent)

        class Profile(BaseRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'AsymmetricTwoRollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(AsymmetricTwoRollPass.DiskElement, self.unit)

        class InProfile(Profile, BaseRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, BaseRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
