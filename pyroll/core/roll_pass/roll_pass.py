import weakref
from typing import List, Union, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, Polygon, MultiPolygon

from ..disk_elements import DiskElementUnit
from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..roll import Roll as BaseRoll
from ..rotator import Rotator
from .deformation_unit import DeformationUnit


class RollPass(DiskElementUnit, DeformationUnit):
    """Represents a roll pass with two symmetric working rolls."""

    rotation = Hook[Union[bool, float]]()
    """
    Rotation applied to the incoming profile in ° (degree) before entry in this roll pass.
    Alternatively, provide a boolean value: false equals 0, 
    true means automatic determination from hook functions of ``Rotator.rotation``.
    """

    gap = Hook[float]()
    """Gap between the rolls (outer surface)."""

    height = Hook[float]()
    """Maximum height of the roll pass."""

    usable_width = Hook[float]()
    """
    Usable width (width of ideal filling).
    Equals the usable width of the groove for two-roll passes, but deviates for three and four-roll passes.
    """

    tip_width = Hook[float]()
    """Width of the intersection of the extended groove flanks (theoretical maximum filling width)."""

    usable_cross_section = Hook[Polygon]()
    """Cross-section of the roll pass at ideal filling with its usable width."""

    tip_cross_section = Hook[Polygon]()
    """Cross-section of the roll pass at filling with its tip width."""

    reappearing_cross_section = Hook[MultiPolygon]()
    """Cross-section of the roll pass witch appears again in the next roll-pass due to spreading."""

    displaced_cross_section = Hook[MultiPolygon]()
    """Cross-section of the roll pass witch is displaced due to elongation and won't reappear in the next roll-pass."""

    roll_force = Hook[float]()
    """Vertical roll force."""

    front_tension = Hook[float]()
    """Front tension acting on the current roll pass."""

    back_tension = Hook[float]()
    """Back tension acting on the current roll pass."""

    elongation_efficiency = Hook[float]()
    """Efficiency of a roll pass to elongate a incoming profile."""

    target_width = Hook[float]()
    """Target width of the out profile."""

    target_filling_ratio = Hook[float]()
    """Target filling ratio of the out profile."""

    target_cross_section_area = Hook[float]()
    """Target cross-section of the out profile."""

    target_cross_section_filling_ratio = Hook[float]()
    """Target cross-section filling ratio of the out profile."""

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

        super().__init__(label=label, **kwargs)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (equal upper and lower)."""

        self._contour_lines = None

    @property
    def contour_lines(self) -> List[LineString]:
        """List of line strings bounding the roll pass at the high point."""
        if self._contour_lines:
            return self._contour_lines

        upper = translate(self.roll.contour_line, yoff=self.gap / 2)
        lower = rotate(upper, angle=180, origin=(0, 0))

        self._contour_lines = [upper, lower]
        return self._contour_lines

    @property
    def classifiers(self):
        """A tuple of keywords to specify the shape type classifiers of this roll pass.
        Shortcut to ``self.groove.classifiers``."""
        return set(self.roll.groove.classifiers)

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def init_solve(self, in_profile: BaseProfile):
        if self.rotation:
            rotator = Rotator(
                # make True determining from hook functions
                rotation=self.rotation if self.rotation is not True else None,
                label=f"Auto-Rotator for {self}",
                duration=0, length=0, parent=self
            )
            rotator.solve(in_profile)
            in_profile = rotator.out_profile

        super().init_solve(in_profile)
        self.out_profile.cross_section = self.usable_cross_section

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    def reevaluate_cache(self):
        super().reevaluate_cache()
        self.roll.reevaluate_cache()
        self._contour_lines = None

    class Profile(DiskElementUnit.Profile, DeformationUnit.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(RollPass, self.unit)

    class InProfile(Profile, DiskElementUnit.InProfile, DeformationUnit.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, DiskElementUnit.OutProfile, DeformationUnit.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()
        """Ratio of profile width to usable width of the groove as width based measure of ideal filling."""

        cross_section_filling_ratio = Hook[float]()
        """Ratio of profile cross-section to usable cross-section of the pass as cross-section based measure of ideal filling."""

        filling_error = Hook[float]()
        """Ratio of profile width to target width as width based measure of target filling."""

        cross_section_error = Hook[float]()
        """Ratio of profile cross-section to target cross-section as cross-section based measure of target filling."""

    class Roll(BaseRoll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: 'RollPass'):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            super().__init__(**kwargs)

            self._roll_pass = weakref.ref(roll_pass)

        @property
        def roll_pass(self):
            """Reference to the roll pass this roll is used in."""
            return self._roll_pass()

    class DiskElement(DiskElementUnit.DiskElement, DeformationUnit):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(RollPass, self.parent)

        class Profile(DiskElementUnit.DiskElement.Profile, DeformationUnit.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'RollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPass.DiskElement, self.unit)

            @property
            def roll_pass(self) -> 'RollPass':
                """Reference to the roll pass. Alias for ``self.unit.parent``"""
                return cast(RollPass, self.unit.parent)

        class InProfile(Profile, DiskElementUnit.DiskElement.InProfile, DeformationUnit.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskElementUnit.DiskElement.OutProfile, DeformationUnit.OutProfile):
            """Represents an outgoing profile of a disk element unit."""

    def plot(self, **kwargs):
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            raise RuntimeError(
                "This method is only available if matplotlib is installed in the environment. "
                "You may install it using the 'plot' extra of pyroll-core."
            ) from e

        fig: plt.Figure = plt.figure(**kwargs)
        ax: plt.Axes
        axl: plt.Axes
        ax, axl = fig.subplots(nrows=2, height_ratios=[1, 0.3])

        if self.label:
            ax.set_title(f"Roll Pass '{self.label}'")

        ax.set_ylabel("y")
        ax.set_xlabel("z")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        c = []
        ipp = []
        ipr = []
        opp = []
        opr = []

        for cl in self.contour_lines:
            c = ax.plot(*cl.xy, color="k", label="roll surface")

        if self.in_profile:
            ipp = ax.fill(*self.in_profile.cross_section.boundary.xy, alpha=0.5, color="red", label="in profile")
            ipr = ax.fill(*self.in_profile.equivalent_rectangle.boundary.xy, fill=False, color="red", ls="--",
                          label="in eq. rectangle")

        if self.out_profile:
            opp = ax.fill(*self.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue", label="out profile")
            opr = ax.fill(*self.out_profile.equivalent_rectangle.boundary.xy, fill=False, color="blue", ls="--",
                          label="out eq. rectangle")

        axl.axis("off")
        axl.legend(handles=c + ipp + opp + ipr + opr, ncols=2, loc="lower center")
        fig.set_layout_engine('constrained')

        return fig
