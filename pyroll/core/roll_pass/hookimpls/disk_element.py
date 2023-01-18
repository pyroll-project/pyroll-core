from ..roll_pass import RollPass


@RollPass.DiskElement.length
def length(self: RollPass.DiskElement):
    return self.roll_pass.roll.contact_length / self.roll_pass.disk_element_count


@RollPass.DiskElement.duration
def disk_duration(self: RollPass.DiskElement):
    return self.length / self.roll_pass.velocity
