import numpy as np
from ..shear import Shear


@Shear.OutProfile.length(
    trylast=True  # do not override getting from in_profile
)
def length_after_cut(self: Shear.OutProfile, cycle):
    if self.has_set_or_cached("length"):
        resulting_length = self.length - self.shear.cut_length
    if resulting_length < 0:
        self.logger.warning("Cut length greater than profile length.")
        return self.length
    else:
        return resulting_length
