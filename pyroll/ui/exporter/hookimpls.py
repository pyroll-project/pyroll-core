import io
import sys

import pandas as pd

from .exporter import Exporter
from ... import RollPass, Unit
from ...utils.hookutils import applies_to_unit_types


@Exporter.hookimpl
@applies_to_unit_types(Unit)
def columns(unit: Unit):
    return dict(
        type=type(unit).__name__,
        label=unit.label
    )


@Exporter.hookimpl
@applies_to_unit_types(RollPass)
def columns(unit: RollPass):
    return dict(
        roll_force=unit.roll_force,
        roll_torque=unit.roll_torque,
        filling_ratio=unit.out_profile.filling_ratio,
        strain_rate=unit.strain_rate,
        contact_area=unit.contact_area,
        contact_length=unit.contact_length
    )


@Exporter.hookimpl(specname="export")
def export_csv(data: pd.DataFrame, export_format: str):
    if not export_format.lower() == "csv":
        return None

    buf = io.BytesIO()
    data.to_csv(buf)

    b = buf.getvalue()
    buf.close()
    return b


@Exporter.hookimpl(specname="export")
def export_xml(data: pd.DataFrame, export_format: str):
    if not export_format.lower() == "xml":
        return None

    buf = io.BytesIO()
    data.to_xml(buf, root_name="sequence", row_name="unit")

    b = buf.getvalue()
    buf.close()
    return b


Exporter.plugin_manager.register(sys.modules[__name__])
