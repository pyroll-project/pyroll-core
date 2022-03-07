import jinja2
from pathlib import Path
from typing import List

import pluggy

from . import utils
from pyroll import RollPass, Unit


def merge_properties(hook_results):
    d = dict()

    for r in hook_results:
        d.update(r)

    return d


class Report:
    plugin_manager = pluggy.PluginManager("pyroll_report")
    hookspec = pluggy.HookspecMarker("pyroll_report")
    hookimpl = pluggy.HookimplMarker("pyroll_report")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
    )

    def render(self, units: List[Unit]) -> str:
        template = self.env.get_template("main.html")

        unit_plots = [
            list(map(
                utils.get_svg_from_figure,
                reversed(
                    self.plugin_manager.hook.unit_plot(unit=u)
                )
            ))
            for u in units
        ]

        unit_properties = [
            merge_properties(self.plugin_manager.hook.unit_properties(unit=u))
            for u in units
        ]

        sequence_plots = map(
            utils.get_svg_from_figure,
            reversed(
                self.plugin_manager.hook.sequence_plot(units=units)
            )
        )

        sequence_properties = merge_properties(self.plugin_manager.hook.sequence_properties(units=units))

        rendered = template.render(
            units=units,
            unit_plots=unit_plots,
            unit_properties=unit_properties,
            unit_infos=zip(units, unit_properties, unit_plots),
            sequence_plots=sequence_plots,
            sequence_properties=sequence_properties
        )

        return rendered
