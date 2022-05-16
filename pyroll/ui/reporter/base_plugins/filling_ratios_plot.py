import sys
from typing import Sequence

import numpy as np

from pyroll.core import RollPass, Unit
from ..reporter import Reporter
from .. import utils


@Reporter.hookimpl
def sequence_plot(units: Sequence[Unit]):
    """Plot the filling ratios of all passes"""
    fig, ax = utils.create_sequence_plot(units)
    ax.set_ylabel(r"filling ratio $i$")
    ax.set_title("Filling Ratios")

    units = list(units)
    if len(units) > 0:
        x, y = np.transpose(
            [
                (index, unit.out_profile.filling_ratio)
                for index, unit in enumerate(units)
                if isinstance(unit, RollPass)
            ]
        )

        ax.bar(x=x, height=y, width=0.8)

        return fig


Reporter.plugin_manager.register(sys.modules[__name__])
