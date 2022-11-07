import sys

from ..roll_pass import RollPass
from ....utils.hookutils import for_in_profile_types, for_roll_pass_types


@RollPass.in_profile_rotation
@for_in_profile_types("diamond")
@for_roll_pass_types("diamond")
def diamonds(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("oval")
@for_roll_pass_types("round")
def oval_round(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("round")
@for_roll_pass_types("oval")
def round_oval(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("oval")
@for_roll_pass_types("square")
def oval_square(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("square")
@for_roll_pass_types("oval")
def square_oval(self):
    return 45


@RollPass.in_profile_rotation
@for_in_profile_types("box")
@for_roll_pass_types("box")
def box_box(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("box")
@for_roll_pass_types("diamond")
def box_diamond(self):
    return 45


@RollPass.in_profile_rotation
@for_in_profile_types("box")
@for_roll_pass_types("oval")
def box_oval(self):
    return 90


@RollPass.in_profile_rotation
@for_in_profile_types("round")
@for_roll_pass_types("flat")
def round_flat(self):
    return 0
