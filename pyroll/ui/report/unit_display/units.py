from pyroll.core import Unit, PassSequence
from ...pluggy import hookimpl, plugin_manager


@hookimpl(specname="report_unit_display", tryfirst=True)
def sequence_heading(unit: Unit, level: int):
    return f"<h{level} class='mt-4'>{str(unit)}</h{level}>"


@hookimpl(specname="report_unit_display")
def sequence_units(unit: Unit, level: int):
    if isinstance(unit, PassSequence):
        displays = "\n".join([
            d
            for u in unit.units
            for d in plugin_manager.hook.report_unit_display(unit=u, level=level + 1)
        ])

        return f"""
        <div>
            {displays}
        </div>
        """
