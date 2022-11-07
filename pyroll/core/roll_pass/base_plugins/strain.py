import logging
import numpy as np

from ..roll_pass import RollPass


@RollPass.strain_change
def strain_change(self: RollPass):
    strain_change = np.log(self.in_profile.cross_section.area / self.out_profile.cross_section.area)

    if strain_change < 0:
        logging.getLogger(__name__).warning(
            "Negative strain change occurred. Assuming it to be zero to be able to continue iteration."
        )
        return 0

    return strain_change


@RollPass.OutProfile.equivalent_strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.equivalent_strain + self.roll_pass.strain_change
