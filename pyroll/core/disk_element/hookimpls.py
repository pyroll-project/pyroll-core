from .disk_element import DiskElement
from .disked_unit import DiskedUnit


@DiskElement.OutProfile.x
def out_x(self: DiskElement.OutProfile):
    return self.disk_element().in_profile.x + self.disk_element().length


@DiskElement.OutProfile.t
def out_t(self: DiskElement.OutProfile):
    return self.disk_element().in_profile.t + self.disk_element().duration


@DiskedUnit.disk_element_count
def no_disks(self: DiskedUnit):
    return 0


@DiskElement.duration
def disk_duration(self: DiskElement):
    return self.parent().duration / self.parent().disk_element_count


@DiskElement.length
def disk_length(self: DiskElement):
    return self.parent().length / self.parent().disk_element_count
