import sys
from collections.abc import Mapping
from typing import Any

import pandas as pd

from .exporter import Exporter


@Exporter.hookspec
def columns(unit) -> Mapping[str, Any]:
    """Take a unit object and extract some data to be listed in the CSV output.
    Return a mapping of column names to values.
    All hookimpls will be joined in order of definition."""


@Exporter.hookspec(firstresult=True)
def export(data: pd.DataFrame, export_format: str) -> bytes:
    """Export the data to a specified format.
    Return binary data that can be saved to a file.
    First hookimpl that does not return None is taken.
    Return None to signal, that the impl does not support the export_format"""


Exporter.plugin_manager.add_hookspecs(sys.modules[__name__])
