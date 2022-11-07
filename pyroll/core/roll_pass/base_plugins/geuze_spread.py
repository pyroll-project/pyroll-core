import logging

from ..roll_pass import RollPass
from ...plugin_host import Hook

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

    if not hasattr(self, "geuze_coefficient"):
        log.warning(f"No Geuze coefficient available for {self.label}.")
        return None

    equivalent_height_change = (self.in_profile.equivalent_rectangle.height
                                - self.out_profile.equivalent_rectangle.height)

    spread = (1 + self.geuze_coefficient * equivalent_height_change
              / self.in_profile.equivalent_rectangle.width)

    log.debug(f"Spread after Geuze: {spread}.")
    return spread
