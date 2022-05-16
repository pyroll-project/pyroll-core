import sys
from typing import Sequence

import numpy as np

from pyroll.core import RollPass, Unit
from ..reporter import Reporter
from .. import utils


@Reporter.hookimpl
def sequence_plot(units: Sequence[Unit]):
    """Plot the roll torques of all passes"""
    fig, ax = utils.create_sequence_plot(units)
    ax.set_ylabel(r"roll torque $M$")
    ax.set_title("Roll Torques")

    units = list(units)
    if len(units) > 0:
        x, y = np.transpose(
            [
                (index, unit.roll.roll_torque)
                for index, unit in enumerate(units)
                if isinstance(unit, RollPass)
            ]
        )

        ax.bar(x=x, height=y, width=0.8)

        return fig


Reporter.plugin_manager.register(sys.modules[__name__])
