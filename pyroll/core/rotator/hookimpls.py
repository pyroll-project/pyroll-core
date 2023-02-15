from .rotator import Rotator
from shapely.affinity import rotate


@Rotator.OutProfile.cross_section
def rotated_cross_section(self: Rotator.OutProfile):
    return rotate(self.rotator.in_profile.cross_section, angle=self.rotator.rotation, origin=(0, 0))


@Rotator.OutProfile.types
def types(self: Rotator.OutProfile):
    r = self.rotator
    t: set = r.in_profile.types | {"rotated"}

    if r.rotation == 45:
        t.add("edged")

    elif r.rotation == 90:
        t.add("vertical")

    elif r.rotation == 180:
        t.add("mirrored")

    return t


@Rotator.rotation
def diamonds(self: Rotator):
    if "diamond" in self.in_profile.types and "diamond" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def oval_round(self: Rotator):
    if "oval" in self.in_profile.types and "round" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def round_oval(self: Rotator):
    if "round" in self.in_profile.types and "oval" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def oval_square(self: Rotator):
    if "oval" in self.in_profile.types and "square" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def square_oval(self: Rotator):
    if "square" in self.in_profile.types and "oval" in self.next_roll_pass.types:
        return 45


@Rotator.rotation
def square_box(self: Rotator):
    if "square" in self.in_profile.types and "box" in self.next_roll_pass.types:
        return 45


@Rotator.rotation
def box_box(self: Rotator):
    if "box" in self.in_profile.types and "box" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def box_diamond(self: Rotator):
    if "box" in self.in_profile.types and "diamond" in self.next_roll_pass.types:
        return 45


@Rotator.rotation
def box_oval(self: Rotator):
    if "box" in self.in_profile.types and "oval" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def round_flat(self: Rotator):
    if "round" in self.in_profile.types and "flat" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def box_flat(self: Rotator):
    if "box" in self.in_profile.types and "flat" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def square_flat(self: Rotator):
    if "square" in self.in_profile.types and "flat" in self.next_roll_pass.types:
        return 45


@Rotator.rotation
def oval_flat(self: Rotator):
    if "oval" in self.in_profile.types and "flat" in self.next_roll_pass.types:
        return 0


@Rotator.rotation
def upset_in(self: Rotator):
    if "upset" in self.in_profile.types:
        return 0


@Rotator.rotation
def upset_out(self: Rotator):
    if "upset" in self.next_roll_pass.types:
        return 90


@Rotator.rotation
def three_roll_pass(self: Rotator):
    if "3fold" in self.next_roll_pass.types:
        return 180
