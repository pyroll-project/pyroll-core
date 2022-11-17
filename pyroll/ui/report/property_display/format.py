import numpy as np

from pyroll.core.repr import ReprMixin
from ...pluggy import hookimpl
from .properties import render_properties_table


@hookimpl(specname="report_property_format")
def int_format(value: object):
    if isinstance(value, int):
        return "{:d}".format(value)


@hookimpl(specname="report_property_format")
def float_format(value: object):
    if isinstance(value, float) or (
            isinstance(value, np.ndarray) and np.isscalar(value) and np.issubdtype(value.dtype, np.floating)):
        order = np.log10(np.abs(value)) // 3
        if not np.isfinite(order):
            return np.format_float_positional(value)
        exp = int(order) * 3
        mantissa = value / 10 ** exp
        return f"{np.format_float_positional(mantissa, trim='0')}e{exp:+03d}"


@hookimpl(specname="report_property_format")
def array_format(value: object):
    if isinstance(value, np.ndarray):
        return np.array_str(value)


@hookimpl(specname="report_property_format")
def repr_mixin_format(value: object):
    if isinstance(value, ReprMixin):
        return render_properties_table(value)


@hookimpl(specname="report_property_format", trylast=True)
def default_format(value: object):
    return str(value)
