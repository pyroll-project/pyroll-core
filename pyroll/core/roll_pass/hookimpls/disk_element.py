from ..roll_pass import RollPass


@RollPass.DiskElement.length
def length(self: RollPass.DiskElement):
    return self.roll_pass.roll.contact_length / self.roll_pass.disk_element_count


@RollPass.DiskElement.duration
def disk_duration(self: RollPass.DiskElement):
    return self.length / self.roll_pass.velocity


@RollPass.DiskElement.InProfile.x
def first_x(self: RollPass.DiskElement.InProfile):
    # only for the first disk element
    if self.disk_element is self.disk_element.roll_pass.disk_elements[0]:
        return self.disk_element.roll_pass.in_profile.x
