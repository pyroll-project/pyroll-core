import jinja2
from pathlib import Path
from typing import List

import pluggy

from . import utils
from pyroll.core import Unit, PassSequence
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
        displays=displays,
    )
