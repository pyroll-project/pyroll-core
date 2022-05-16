from typing import List
import pandas as pd

import pluggy

from pyroll.core import Unit


class Exporter:
    """Class able to export simulation results to several data formats."""

    plugin_manager = pluggy.PluginManager("pyroll_csv_exporter")
    hookspec = pluggy.HookspecMarker("pyroll_csv_exporter")
    hookimpl = pluggy.HookimplMarker("pyroll_csv_exporter")

    def get_columns(self, unit):
        results = self.plugin_manager.hook.columns(unit=unit)

        columns = dict()

        for r in results:
            columns.update(r)

        return columns

    def get_dataframe(self, units: List[Unit]) -> pd.DataFrame:
        """
        Generate a pandas DataFrame by use of the unit_columns, roll_pass_columns and transport_columns hooks.

        :param units: list of units to take the data from
        :returns: a pandas data frame filled with the exported data
        """
        rows = [
            self.get_columns(unit)
            for unit in units
        ]

        df = pd.DataFrame(rows)
        df.index.name = "id"
        return df

    def export(self, units: List[Unit], export_format: str) -> bytes:
        """
        Call get_dataframe and export its results to a specified format.

        :param units: list of units to take the data from
        :param export_format: a string key identifying the export format,
            valid values depend on the loaded implementations of the 'export' hook
        :returns: the exported data as binary stream
        """
        data = self.get_dataframe(units)
        return Exporter.plugin_manager.hook.export(data=data, export_format=export_format)
