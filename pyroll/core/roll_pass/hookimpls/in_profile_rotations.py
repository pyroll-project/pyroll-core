from ..roll_pass import RollPass


@RollPass.in_profile_rotation
def diamonds(self: RollPass):
    if "diamond" in self.in_profile.types and "diamond" in self.types:
        return 90


@RollPass.in_profile_rotation
def oval_round(self: RollPass):
    if "oval" in self.in_profile.types and "round" in self.types:
        return 90


@RollPass.in_profile_rotation
def round_oval(self: RollPass):
    if "round" in self.in_profile.types and "oval" in self.types:
        return 90


@RollPass.in_profile_rotation
def oval_square(self: RollPass):
    if "oval" in self.in_profile.types and "square" in self.types:
        return 90


@RollPass.in_profile_rotation
def square_oval(self: RollPass):
    if "square" in self.in_profile.types and "oval" in self.types:
     return 45


@RollPass.in_profile_rotation
def box_box(self: RollPass):
    if "box" in self.in_profile.types and "box" in self.types:
        return 90


@RollPass.in_profile_rotation
def box_diamond(self: RollPass):
    if "box" in self.in_profile.types and "diamond" in self.types:
        return 45


@RollPass.in_profile_rotation
def box_oval(self: RollPass):
    if "box" in self.in_profile.types and "oval" in self.types:
        return 90


@RollPass.in_profile_rotation
def round_flat(self: RollPass):
    if "round" in self.in_profile.types and "flat" in self.types:
        return 0
