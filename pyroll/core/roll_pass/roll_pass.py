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

    orientation = Hook[Union[int, str]]()
    """
    Orientation of the roll pass for displaying purposes. 
    Meaning of height and width always refer to standard horizontal orientation anyway.
    Commonly 0 (horizontal) or 90 (vertical) for two-roll passes. Other integer values are supported, too.
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

    entry_point = Hook[float]()
    """Point where the material enters the roll gap."""

    entry_angle = Hook[float]()
    """Angle at which the material enters the roll gap."""

    exit_point = Hook[float]()
    """Point where the material exits the roll gap."""

    exit_angle = Hook[float]()
    """Angle at which the material exits the roll gap."""

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

    forward_slip_ratio = Hook[float]()
    """Ratio of forward slip of the roll gap."""

    location = Hook[float]()
    """Coordinate of the passes high point in rolling direction."""

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
        from pyroll.core import PLOTTING_BACKEND
        if PLOTTING_BACKEND is None:
            raise RuntimeError(
                "This method is only available if matplotlib or plotly is installed in the environment. "
                "You may install one of them using the 'plot', 'matplotlib' or 'plotly' extras of pyroll-core."
            )

        def oriented(geom):
            orientation = self.orientation

            if isinstance(orientation, str):
                if orientation.lower() in ["horizontal", "h", "y"]:
                    orientation = 0
                elif orientation.lower() in ["vertical", "v"]:
                    orientation = 90
                elif orientation.lower() in ["antiy", "ay"]:
                    orientation = 180

            if orientation != 0:
                return rotate(geom, orientation, (0, 0))
            return geom

        if PLOTTING_BACKEND == "matplotlib":
            import matplotlib.pyplot as plt

            fig: plt.Figure = plt.figure(**kwargs)
            ax: plt.Axes
            axl: plt.Axes
            ax = fig.subplots()

            if self.label:
                ax.set_title(f"Roll Pass '{self.label}'")

            ax.set_ylabel("y")
            ax.set_xlabel("z")

            ax.set_aspect("equal", "datalim")
            ax.grid(lw=0.5)

            artists = []

            if self.in_profile:
                artists += ax.fill(
                    *oriented(self.in_profile.cross_section.boundary).xy,
                    alpha=0.5, color="red", label="in profile"
                )
                artists += ax.fill(
                    *oriented(self.in_profile.equivalent_rectangle.boundary).xy,
                    fill=False, color="red", ls="--", label="in eq. rectangle"
                )

            if self.out_profile:
                artists += ax.fill(
                    *oriented(self.out_profile.cross_section.boundary).xy,
                    alpha=0.5, color="blue", label="out profile"
                )
                artists += ax.fill(
                    *oriented(self.out_profile.equivalent_rectangle.boundary).xy,
                    fill=False, color="blue", ls="--", label="out eq. rectangle"
                )

            c = None
            for cl in self.contour_lines:
                c = ax.plot(*oriented(cl).xy, color="k", label="roll surface")

            if c is not None:
                artists += c

            ncols = len(artists) // 2 + 1

            ax.legend(handles=artists, ncols=ncols, loc='lower center')
            fig.set_layout_engine('constrained')

            return fig

        if PLOTTING_BACKEND == "plotly":
            import plotly.graph_objects as go

            fig = go.Figure(layout=go.Layout(
                xaxis=dict(
                    title="z",
                ),
                yaxis=dict(
                    title="y",
                    scaleanchor="x",
                    scaleratio=1
                ),
                title=f"Roll Pass '{self.label}'" if self.label else None,
                template="simple_white"
            ))

            if self.in_profile:
                coords = oriented(self.in_profile.cross_section.boundary).xy
                fig.add_trace(go.Scatter(
                    x=np.array(coords[0]),
                    y=np.array(coords[1]),
                    mode="lines",
                    fill="toself",
                    line=dict(color="red"),
                    name="in profile"
                ))
                coords = oriented(self.in_profile.equivalent_rectangle.boundary).xy
                fig.add_trace(go.Scatter(
                    x=np.array(coords[0]),
                    y=np.array(coords[1]),
                    mode="lines",
                    line=dict(color="red", dash="dash"),
                    name="in eq. rectangle"
                ))

            if self.out_profile:
                coords = oriented(self.out_profile.cross_section.boundary).xy
                fig.add_trace(go.Scatter(
                    x=np.array(coords[0]),
                    y=np.array(coords[1]),
                    mode="lines",
                    fill="toself",
                    line=dict(color="blue"),
                    name="out profile"
                ))
                coords = oriented(self.out_profile.equivalent_rectangle.boundary).xy
                fig.add_trace(go.Scatter(
                    x=np.array(coords[0]),
                    y=np.array(coords[1]),
                    mode="lines",
                    line=dict(color="blue", dash="dash"),
                    name="out eq. rectangle"
                ))

            show_in_legend = True
            for cl in self.contour_lines:
                coords = oriented(cl).xy
                fig.add_trace(go.Scatter(
                    x=np.array(coords[0]),
                    y=np.array(coords[1]),
                    mode="lines",
                    line=dict(color="black"),
                    name="roll surface",
                    showlegend=show_in_legend
                ))
                show_in_legend = False

            return fig
