import sys
from typing import Sequence

import numpy as np

from pyroll.core import Unit
from ..reporter import Reporter
from .. import utils


@Reporter.hookimpl
def sequence_plot(units: Sequence[Unit]):
    """Plot the strains of all profiles"""
    fig, ax = utils.create_sequence_plot(units)
    ax.set_ylabel(r"strain $\varphi_\mathrm{V}$")
    ax.set_title("Mean Equivalent Strains")

    units = list(units)
    if len(units) > 0:
        def gen_seq():
            yield -0.5, units[0].in_profile.strain
            for i, u in enumerate(units):
                yield i + 0.5, u.out_profile.strain

        x, y = np.transpose(
            list(gen_seq())
        )

        ax.plot(x, y, marker="x")

        return fig


Reporter.plugin_manager.register(sys.modules[__name__])
