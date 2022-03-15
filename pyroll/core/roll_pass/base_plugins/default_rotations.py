import sys

from ..roll_pass import RollPass
from ....utils.hookutils import applies_to_in_grooves, applies_to_out_grooves
from ... import grooves
from ...grooves.boxes import BoxGrooveBase


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(grooves.DiamondGrooveBase)
@applies_to_out_grooves(grooves.DiamondGrooveBase)
def diamonds(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(grooves.OvalGrooveBase)
@applies_to_out_grooves(grooves.RoundGrooveBase)
def oval_round(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(grooves.RoundGrooveBase)
@applies_to_out_grooves(grooves.OvalGrooveBase)
def round_oval(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(grooves.OvalGrooveBase)
@applies_to_out_grooves(grooves.SquareGroove)
def oval_square(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(grooves.SquareGroove)
@applies_to_out_grooves(grooves.OvalGrooveBase)
def square_oval(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(BoxGrooveBase)
@applies_to_out_grooves(BoxGrooveBase)
def box_box(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(BoxGrooveBase)
@applies_to_out_grooves(grooves.DiamondGrooveBase)
def box_diamond(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves(BoxGrooveBase)
@applies_to_out_grooves(grooves.OvalGrooveBase)
def box_oval(roll_pass):
    return 90


RollPass.plugin_manager.register(sys.modules[__name__])
