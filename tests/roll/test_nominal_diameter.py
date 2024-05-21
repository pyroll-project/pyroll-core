from pyroll.core import Roll, RoundGroove
from numpy import isclose


def test_nominal_diameter_input():
    roll = Roll(
        groove=RoundGroove(r1=2, r2=10, depth=10),
        nominal_diameter=200,
        contact_length=50
    )
    assert isclose(roll.nominal_radius, 100)
