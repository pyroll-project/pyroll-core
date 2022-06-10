import sys

from ..roll_pass import RollPass
from ....utils.hookutils import for_in_profile_types, for_roll_pass_types


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("diamond")
@for_roll_pass_types("diamond")
def diamonds(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("oval")
@for_roll_pass_types("round")
def oval_round(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("round")
@for_roll_pass_types("oval")
def round_oval(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("oval")
@for_roll_pass_types("square")
def oval_square(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("square")
@for_roll_pass_types("oval")
def square_oval(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("box")
@for_roll_pass_types("box")
def box_box(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("box")
@for_roll_pass_types("diamond")
def box_diamond(roll_pass):
    return 45


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("box")
@for_roll_pass_types("oval")
def box_oval(roll_pass):
    return 90


@RollPass.hookimpl(specname="in_profile_rotation")
@for_in_profile_types("round")
@for_roll_pass_types("flat")
def round_flat(roll_pass):
    return 0


RollPass.plugin_manager.register(sys.modules[__name__])
