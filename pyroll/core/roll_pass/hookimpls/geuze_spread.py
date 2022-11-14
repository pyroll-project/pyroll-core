import logging

from ..roll_pass import RollPass
from ...hooks import Hook

RollPass.geuze_coefficient = Hook[float]()


@RollPass.geuze_coefficient
def geuze_coefficient(self: RollPass):
    """Backup coefficient = 0.3"""
    return 0.3


@RollPass.spread
def spread(self: RollPass):
    """
    Geuze spreading model: Δb = c * Δh

    :param self: roll setup
    :type self: Unit
    :return: spread of the material
    :rtype: float
    """
    log = logging.getLogger(__name__)

    if hasattr(self, "geuze_coefficient"):
        equivalent_height_change = (self.in_profile.equivalent_rectangle.height
                                    - self.out_profile.equivalent_rectangle.height)

        spread = (1 + self.geuze_coefficient * equivalent_height_change
                  / self.in_profile.equivalent_rectangle.width)

        log.debug(f"Spread after Geuze: {spread}.")
        return spread


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    if "width" in self.__dict__:
        return self.roll_pass().in_profile.width * self.roll_pass().spread


RollPass.root_hooks.add(RollPass.OutProfile.width)
