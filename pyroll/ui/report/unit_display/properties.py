from pathlib import Path

import jinja2

from pyroll.core import Unit
from pyroll.core.repr import ReprMixin
from pyroll.ui.pluggy import hookimpl, plugin_manager

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)


class DoNotPrint(Exception):
    pass


def try_format_property(name: str, value: object):
    try:
        return plugin_manager.hook.report_property_format(name=name, value=value)
    except (TypeError, ValueError, DoNotPrint):
        return None


def render_properties_table(instance: ReprMixin):
    template = _env.get_template("properties.html")

    properties = [
        (n, s) for n, v in instance.__attrs__.items()
        if (s := try_format_property(n, v)) is not None
    ]

    return template.render(
        properties=properties,
    )


@hookimpl(specname="report_unit_display")
def unit_property_display(unit: Unit, level: int):
    return render_properties_table(unit)
