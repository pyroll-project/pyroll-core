import re
from io import StringIO
from typing import Sequence

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

from pyroll.core import Unit


def create_sequence_plot(units: Sequence[Unit]):
    """Creates a styled base figure for use in sequence plots.
    The x-axis ticks will be labeled with the unit labels and indices."""
    fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(6, 4))
    ax: plt.Axes = fig.subplots()

    indices = np.arange(len(units))
    ax.xaxis.set_major_locator(FixedLocator(indices))
    ax.xaxis.set_major_formatter(
        FixedFormatter([(f"{i}: {p.label}" if p.label else str(i)) for i, p in zip(indices, units)]))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    ax.grid()

    return fig, ax


def resize_svg_to_100_percent(svg: str) -> str:
    svg = re.sub(r'height="[\d.\w]*?"', 'height="100%"', svg)
    svg = re.sub(r'width="[\d.\w]*?"', 'width="100%"', svg)
    return svg


def get_svg_from_figure(fig: plt.Figure) -> str:
    with StringIO() as buf:
        fig.savefig(buf, format="svg")
        plt.close(fig)
        return resize_svg_to_100_percent(buf.getvalue())
