import sys
from typing import Sequence

import numpy as np

from pyroll import RollPass, Unit
from ..report import Report
from .. import utils


@Report.hookimpl
def sequence_plot(units: Sequence[Unit]):
    """Plot the roll forces of all passes"""
    fig, ax = utils.create_sequence_plot(units)
    ax.set_ylabel(r"roll force $F$")
    ax.set_title("Roll Forces")

    units = list(units)
    if len(units) > 0:
        indices, forces = np.transpose(
            [
                (index, unit.roll_force)
                for index, unit in enumerate(units)
                if isinstance(unit, RollPass)
            ]
        )

        ax.bar(x=indices, height=forces, width=0.8)

        return fig


Report.plugin_manager.register(sys.modules[__name__])
