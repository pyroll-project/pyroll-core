import sys
from typing import List, Tuple, Mapping, Any

from matplotlib.figure import Figure

from .reporter import Reporter
from pyroll.core import Unit


@Reporter.hookspec()
def unit_plot(unit: Unit) -> Figure:
    """Generate a matplotlib figure visualizing a unit.
    All loaded hook implementations are listed in the report."""


@Reporter.hookspec
def sequence_plot(units: List[Unit]) -> Figure:
    """Generate a matplotlib figure visualizing the whole pass sequence,
    f.e. plot the distribution of roll forces.
    All loaded hook implementations are listed in the report."""


@Reporter.hookspec
def unit_properties(unit: Unit) -> Mapping[str, Any]:
    """Extract some data from a unit to be listed in the report.
    Return a mapping of label names to values.
    All hookimpls will be joined in order of definition."""


@Reporter.hookspec
def sequence_properties(units: List[Unit]) -> Mapping[str, Any]:
    """Extract some data from the unit sequence to be listed in the report.
    Return a mapping of label names to values.
    All hookimpls will be joined in order of definition."""


Reporter.plugin_manager.add_hookspecs(sys.modules[__name__])
