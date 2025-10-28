from abc import ABC
from typing import List, cast

import weakref
import numpy as np
from ..hooks import Hook
from .base import BaseRollPass
from ..roll import Roll as BaseRoll
from ..engine import Engine as BaseEngine

__all__ = ["SymmetricRollPass"]


class SymmetricRollPass(BaseRollPass, ABC):
    """Represents a symmetric roll pass with equal upper and lower working roll."""

    def __init__(self, roll: BaseRoll, engine: BaseEngine = BaseEngine(), label: str = "", **kwargs):
        super().__init__(label, **kwargs)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (all equal)."""

        self.engine = self.Engine(engine, self)
        """The engine of this pass."""

    @property
    def disk_elements(self) -> List["SymmetricRollPass.DiskElement"]:
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
        engine_results = self.engine.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results, engine_results], axis=0)

    def reevaluate_cache(self):
        super().reevaluate_cache()
        self.roll.reevaluate_cache()
        self._contour_lines = None
        self.engine.reevaluate_cache()

    class Profile(BaseRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> "SymmetricRollPass":
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(SymmetricRollPass, self.unit)

    class InProfile(Profile, BaseRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, BaseRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

    class Roll(BaseRoll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: "SymmetricRollPass"):
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

    class Engine(BaseRollPass.Engine):
        """Represents an engine applied in a :py:class:`RollPass`."""

        @property
        def roll_pass(self) -> "SymmetricRollPass":
            """Reference to the roll pass."""
            return cast(SymmetricRollPass, self._roll_pass())

    class DiskElement(BaseRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> "SymmetricRollPass":
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(SymmetricRollPass, self.parent)

        class Profile(BaseRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> "SymmetricRollPass.DiskElement":
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(SymmetricRollPass.DiskElement, self.unit)

        class InProfile(Profile, BaseRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, BaseRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
