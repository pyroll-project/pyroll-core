from .disked_unit import DiskedUnit


@DiskedUnit.disk_element_count
def no_disks(self: DiskedUnit):
    return 0


@DiskedUnit.DiskElement.duration
def disk_duration(self: DiskedUnit.DiskElement):
    return self.parent.duration / self.parent.disk_element_count


@DiskedUnit.DiskElement.length
def disk_length(self: DiskedUnit.DiskElement):
    return self.parent.length / self.parent.disk_element_count
