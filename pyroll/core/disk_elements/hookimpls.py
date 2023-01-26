from .disk_element_unit import DiskElementUnit


@DiskElementUnit.disk_element_count
def no_disks(self: DiskElementUnit):
    return 0


@DiskElementUnit.DiskElement.duration
def disk_duration(self: DiskElementUnit.DiskElement):
    return self.parent.duration / self.parent.disk_element_count


@DiskElementUnit.DiskElement.length
def disk_length(self: DiskElementUnit.DiskElement):
    return self.parent.length / self.parent.disk_element_count
