from matplotlib.figure import Figure

from ..pluggy import hookspec
from pyroll.core import Unit


@hookspec
def report_unit_display(unit: Unit, level: int) -> str:
    """Return HTML code as str which displays the given unit.
    Multiple implementations will be included sequentially into the report.
    Other return types as HTML str are possible, if respective hook wrappers for conversion exist."""


@hookspec
def report_unit_plot(unit: Unit) -> Figure | str:
    """Generate a matplotlib figure or SVG code visualizing a unit.
    All loaded hook implementations are listed in the report."""


@hookspec(firstresult=True)
def report_property_format(name: str, value: object) -> str:
    """Format the value of a property as string for display in the report. This hook is first result."""
