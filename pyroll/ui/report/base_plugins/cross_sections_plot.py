import sys
from typing import Sequence

import numpy as np

from pyroll import RollPass, Unit
from ..report import Report
from .. import utils


@Report.hookimpl
def sequence_plot(units: Sequence[Unit]):
    """Plot the strains of all profiles"""
    fig, ax = utils.create_sequence_plot(units)
    ax.set_ylabel(r"cross section $A_\mathrm{p}$")
    ax.set_title("Profile Cross Sections")

    units = list(units)
    if len(units) > 0:
        def gen_seq():
            yield -0.5, units[0].in_profile.cross_section
            for i, u in enumerate(units):
                if isinstance(u, RollPass):
                    yield i + 0.5, u.out_profile.cross_section

        x, y = np.transpose(
            list(gen_seq())
        )

        ax.plot(x, y, marker="x")

        return fig


Report.plugin_manager.register(sys.modules[__name__])
