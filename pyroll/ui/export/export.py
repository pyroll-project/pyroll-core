from typing import Any

from .convert import _to_dict
from pyroll.core import Unit


def to_dict(unit: Unit) -> dict[str, Any]:
    d = _to_dict(unit)

    print(d)
    return d
