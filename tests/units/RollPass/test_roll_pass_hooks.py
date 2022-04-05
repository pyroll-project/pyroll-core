import pytest

from pyroll import RollPass
from pyroll.core.grooves import RoundGroove

groove_dummy = RoundGroove(r1=1, r2=10, depth=9)


class Specs:
    @RollPass.hookspec
    def hook1(self, roll_pass):
        """"""


RollPass.plugin_manager.add_hookspecs(Specs())


def test_hook_not_present():
    roll_pass = RollPass(groove=groove_dummy)

    with pytest.raises(AttributeError):
        print(roll_pass.does_not_exist)


def test_hook_result_none():
    roll_pass = RollPass(groove=groove_dummy)

    with pytest.raises(AttributeError):
        print(roll_pass.hook1)


def test_hook():
    roll_pass = RollPass(groove=groove_dummy, gap=1)
    print(roll_pass.tip_width)
