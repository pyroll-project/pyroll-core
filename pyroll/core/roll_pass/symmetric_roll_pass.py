from abc import ABC
from typing import List, cast

import numpy as np
from .base import BaseRollPass
from ..roll import Roll as BaseRoll


class SymmetricRollPass(BaseRollPass, ABC):
    """Represents a symmetric roll pass with equal upper and lower working roll."""

    def __init__(
            self,
            roll: BaseRoll,
            label: str = "",
            **kwargs
    ):
        super().__init__(label, **kwargs)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (all equal)."""

    @property
    def disk_elements(self) -> List['SymmetricRollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    @property
    def classifiers(self):
        """A tuple of keywords to specify the shape type classifiers of this roll pass.
        Shortcut to ``self.groove.classifiers``."""
        return set(self.roll.groove.classifiers) | {"symmetric"}

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    def reevaluate_cache(self):
        super().reevaluate_cache()
        self.roll.reevaluate_cache()
        self._contour_lines = None

    class Profile(BaseRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'SymmetricRollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(SymmetricRollPass, self.unit)

    class InProfile(Profile, BaseRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, BaseRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

    class Roll(BaseRollPass.Roll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        @property
        def roll_pass(self) -> 'SymmetricRollPass':
            """Reference to the roll pass."""
            return cast(SymmetricRollPass, self._roll_pass())

    class DiskElement(BaseRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'SymmetricRollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(SymmetricRollPass, self.parent)

        class Profile(BaseRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'SymmetricRollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(SymmetricRollPass.DiskElement, self.unit)

        class InProfile(Profile, BaseRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, BaseRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
