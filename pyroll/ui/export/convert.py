from typing import Sequence, Any

import numpy as np

from ..pluggy import hookimpl, plugin_manager
from ...core.repr import ReprMixin


def _to_dict(instance: ReprMixin):
    return {
        n: plugin_manager.hook.export_convert(name=n, value=v) for n, v in instance.__attrs__.items()
    }


def _flatten_dict(d: dict[str, Any]) -> dict[str | tuple[str, ...], Any]:
    def _gen(d_: dict[str, Any], prefix=()):
        for k, v in d_.items():
            if isinstance(v, dict):
                yield from _gen(v, prefix + (k,))
            else:
                yield prefix + (k,), v

    return dict((".".join(k), v) for k, v in _gen(d))


@hookimpl(specname="export_convert")
def convert_repr_mixin(value: object):
    if isinstance(value, ReprMixin):
        return _to_dict(value)


@hookimpl(specname="export_convert")
def convert_str_sequence(name: str, value: object):
    if isinstance(value, Sequence) and not isinstance(value, str):
        try:
            return ", ".join(value)
        except TypeError:
            return None


@hookimpl(specname="export_convert")
def convert_sequence(name: str, value: object):
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [plugin_manager.hook.export_convert(name=f"{name}[{i}]", value=v) for i, v in enumerate(value)]


@hookimpl(specname="export_convert")
def convert_array(value: object):
    if isinstance(value, np.ndarray):
        squeezed = value.squeeze()
        if squeezed.ndim == 0:
            return squeezed[()]
        return value


@hookimpl(specname="export_convert")
def convert_primitives(value: object):
    if isinstance(value, (float, str, int, bool, bytes)):
        return value


@hookimpl(specname="export_convert")
def convert_default():
    return None
