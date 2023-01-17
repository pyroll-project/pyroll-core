from .disk_element import DiskElement
from .disked_unit import DiskedUnit


@DiskedUnit.disk_element_count
def no_disks(self: DiskedUnit):
    return 0


@DiskElement.duration
def disk_duration(self: DiskElement):
    return self.parent().duration / self.parent().disk_element_count


@DiskElement.length
def disk_length(self: DiskElement):
    return self.parent().length / self.parent().disk_element_count
