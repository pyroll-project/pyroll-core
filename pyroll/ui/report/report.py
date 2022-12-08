import datetime

import jinja2
from pathlib import Path
import platform

from pyroll.core import PassSequence
from ..pluggy import plugin_manager

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)


def report(pass_sequence: PassSequence) -> str:
    """
    Render an HTML report from the specified units list.

    :param pass_sequence: list of units to take the data from
    :returns: generated HTML code as string
    """

    template = _env.get_template("main.html")

    displays = plugin_manager.hook.report_unit_display(unit=pass_sequence, level=1)

    return template.render(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        platform=f"{platform.node()} ({platform.platform()}, {platform.python_implementation()} {platform.python_version()})",
        displays=displays,
    )
