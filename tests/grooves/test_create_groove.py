import pyroll.core as pr
import pytest


@pytest.mark.parametrize(
    ["name", "args", "expected_class"],
    [
        ("box", dict(r1=1, r2=1, usable_width=10, depth=3, flank_angle=80), pr.BoxGroove),
        ("circular oval", dict(r1=1, r2=20, depth=3), pr.CircularOvalGroove),
        ("circular-oval", dict(r1=1, r2=20, depth=3), pr.CircularOvalGroove),
        ("circular_oval", dict(r1=1, r2=20, depth=3), pr.CircularOvalGroove),
        ("circular Oval", dict(r1=1, r2=20, depth=3), pr.CircularOvalGroove),
        ("swedish-oval groove", dict(r1=1, r2=1, depth=3, usable_width=10, ground_width=6), pr.SwedishOvalGroove),
    ],
)
def test_create_groove(name: str, args: dict, expected_class: type):
    inst = pr.create_groove_by_type_name(name, **args)

    assert isinstance(inst, expected_class)
