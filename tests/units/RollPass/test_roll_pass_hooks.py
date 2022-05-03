import numpy as np
import pytest

from pyroll import RollPass, Roll
from pyroll.core.grooves import RoundGroove

groove_dummy = RoundGroove(r1=1, r2=10, depth=9)
roll_dummy = Roll(groove=groove_dummy)


class Specs:
    @RollPass.hookspec
    def hook1(self, roll_pass):
        """"""


RollPass.plugin_manager.add_hookspecs(Specs())


def test_hook_not_present():
    roll_pass = RollPass(roll=roll_dummy)

    with pytest.raises(AttributeError):
        print(roll_pass.does_not_exist)


def test_hook_result_none():
    roll_pass = RollPass(roll=roll_dummy)

    with pytest.raises(AttributeError):
        print(roll_pass.hook1)


def test_hook_result_nan():
    class Impls:
        @staticmethod
        @RollPass.hookimpl
        def hook1():
            return np.nan

    RollPass.plugin_manager.register(Impls)

    roll_pass = RollPass(roll=roll_dummy)

    with pytest.raises(ValueError):
        print(roll_pass.hook1)


def test_hook():
    roll_pass = RollPass(roll=roll_dummy, gap=1)
    print(roll_pass.tip_width)
