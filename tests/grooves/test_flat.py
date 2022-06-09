from numpy import isclose
from pyroll.core import FlatGroove


def test_flat():
    g = FlatGroove(width=100)

    assert isclose(g.usable_width, 100)