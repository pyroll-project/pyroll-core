from pathlib import Path

import jinja2

from pyroll.core import Unit
from pyroll.core.repr import ReprMixin
from ...pluggy import hookimpl, plugin_manager

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)


def render_properties_table(instance: ReprMixin):
    template = _env.get_template("properties.html")

    properties = [
        (n, plugin_manager.hook.report_property_format(value=v)) for n, v in instance.__attrs__.items()
    ]

    return template.render(
        properties=properties,
    )


# @hookimpl(specname="report_unit_display", tryfirst=True)
# def sequence_property_display(unit: Unit, level: int):
#     if isinstance(unit, PassSequence):
#         return render_properties_table(unit)


@hookimpl(specname="report_unit_display", tryfirst=True)
def unit_property_display(unit: Unit, level: int):
    return render_properties_table(unit)
