from .rotator import Rotator
from shapely.affinity import rotate


@Rotator.duration
def duration(self: Rotator):
    return 0


@Rotator.OutProfile.cross_section
def rotated_cross_section(self: Rotator.OutProfile):
    return rotate(self.rotator.in_profile.cross_section, angle=self.rotator.rotation, origin=(0, 0))


@Rotator.OutProfile.classifiers
def classifiers(self: Rotator.OutProfile):
    r = self.rotator
    t: set = r.in_profile.classifiers | {"rotated"}

    if r.rotation == 45:
        t.add("edged")

    elif r.rotation == 90:
        t.add("vertical")

    elif r.rotation == 180:
        t.add("mirrored")

    return t


@Rotator.rotation
def default_90(self: Rotator):
    return 90


@Rotator.rotation
def square_oval_45(self: Rotator):
    if "square" in self.in_profile.classifiers and "oval" in self.next_roll_pass.classifiers:
        return 45


@Rotator.rotation
def square_box_45(self: Rotator):
    if "square" in self.in_profile.classifiers and "box" in self.next_roll_pass.classifiers:
        return 45


@Rotator.rotation
def box_diamond_45(self: Rotator):
    if "box" in self.in_profile.classifiers and "diamond" in self.next_roll_pass.classifiers:
        return 45


@Rotator.rotation
def box_flat_0(self: Rotator):
    if "box" in self.in_profile.classifiers and "flat" in self.next_roll_pass.classifiers:
        return 0


@Rotator.rotation
def square_flat_45(self: Rotator):
    if "square" in self.in_profile.classifiers and "flat" in self.next_roll_pass.classifiers:
        return 45


@Rotator.rotation
def oval_flat_0(self: Rotator):
    if "oval" in self.in_profile.classifiers and "flat" in self.next_roll_pass.classifiers:
        return 0


@Rotator.rotation
def upset_in_0(self: Rotator):
    if "upset" in self.in_profile.classifiers:
        return 0


@Rotator.rotation
def three_roll_pass_180(self: Rotator):
    if "3fold" in self.next_roll_pass.classifiers:
        return 180
