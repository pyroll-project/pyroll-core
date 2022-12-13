from .rotator import Rotator
from shapely.affinity import rotate


@Rotator.OutProfile.cross_section
def rotated_cross_section(self: Rotator.OutProfile):
    r = self.rotator()
    return rotate(r.in_profile.cross_section, angle=r.rotation, origin=(0, 0))
