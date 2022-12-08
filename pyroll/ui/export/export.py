from typing import Any, Sequence

import pandas as pd

from .convert import _to_dict, _flatten_dict
from pyroll.core import Unit
import json


def to_dict(unit: Unit) -> dict[str, Any]:
    return _to_dict(unit)


def to_pandas(sequence: Sequence[Unit]) -> pd.DataFrame:
    df = pd.DataFrame([
        _flatten_dict(_to_dict(u)) for u in sequence
    ])
    df.sort_index(axis="columns", inplace=True)
    return df.convert_dtypes()


def to_json(unit: Unit) -> str:
    return json.dumps(to_dict(unit), indent=4)
