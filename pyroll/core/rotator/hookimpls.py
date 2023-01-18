from .rotator import Rotator
from shapely.affinity import rotate


@Rotator.OutProfile.cross_section
def rotated_cross_section(self: Rotator.OutProfile):
    return rotate(self.rotator.in_profile.cross_section, angle=self.rotator.rotation, origin=(0, 0))
