from typing import Optional

import numpy as np

from .base import BoxGrooveBase


class BoxGroove(BoxGrooveBase):

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: float,
            ground_width: Optional[float] = None,
            usable_width: Optional[float] = None,
            flank_angle: Optional[float] = None
    ):
        if ground_width and usable_width and not flank_angle:
            flank_angle = np.arctan(depth / (usable_width - ground_width) * 2)
        elif usable_width and flank_angle and not ground_width:
            ground_width = usable_width - 2 * depth / np.tan(flank_angle)
        elif ground_width and flank_angle and not usable_width:
            usable_width = ground_width + 2 * depth / np.tan(flank_angle)
        else:
            raise ValueError(
                "Exactly two of the following arguments must be given: ground_width, usable_width, flank_angle must be given."
            )

        even_ground_width = ground_width - 2 * r2 * np.tan(flank_angle / 2)

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=flank_angle, alpha2=flank_angle,
                         even_ground_width=even_ground_width)

        self.bachtinow_shternov_first_radius_test(lower_bound=0.8, upper_bound=1.0, dependent_value=self.r1)
        self.bachtinow_shternov_second_radius_test(lower_bound=0.08, upper_bound=1.0, dependent_value=self.depth)

    def __str__(self):
        return 'BoxGroove {}'.format(self.groove_label)
