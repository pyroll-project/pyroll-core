import sys

from ..roll_pass import RollPass
from ....utils.hookutils import applies_to_in_grooves, applies_to_out_grooves


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("diamond")
@applies_to_out_grooves("diamond")
def diamonds(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("oval")
@applies_to_out_grooves("round")
def oval_round(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("round")
@applies_to_out_grooves("oval")
def round_oval(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("oval")
@applies_to_out_grooves("square")
def oval_square(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("square")
@applies_to_out_grooves("oval")
def square_oval(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("box")
@applies_to_out_grooves("box")
def box_box(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("box")
@applies_to_out_grooves("diamond")
def box_diamond(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("box")
@applies_to_out_grooves("oval")
def box_oval(roll_pass):
    return 90


RollPass.plugin_manager.register(sys.modules[__name__])
