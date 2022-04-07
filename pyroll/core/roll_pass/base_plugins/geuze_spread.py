import logging

from ..roll_pass import RollPass


class Specs:
    @staticmethod
    @RollPass.hookspec
    def geuze_coefficient(roll_pass: RollPass):
        """Geuze spreading coefficient."""


class Impls:
    @staticmethod
    @RollPass.hookimpl
    def geuze_coefficient(roll_pass: RollPass):
        """Backup coefficient = 0.3"""
        return 0.3

    @staticmethod
    @RollPass.hookimpl
    def spread(roll_pass: RollPass):
        """
        Geuze spreading model: Δb = c * Δh

        :param roll_pass: roll setup
        :type roll_pass: Unit
        :return: spread of the material
        :rtype: float
        """
        log = logging.getLogger(__name__)

        if not hasattr(roll_pass, "geuze_coefficient"):
            log.warning(f"No Geuze coefficient available for {roll_pass.label}.")
            return None

        equivalent_height_change = (roll_pass.in_profile.equivalent_rectangle.height
                                    - roll_pass.out_profile.equivalent_rectangle.height)

        spread = (1 + roll_pass.geuze_coefficient * equivalent_height_change
                  / roll_pass.in_profile.equivalent_rectangle.width)

        log.debug(f"Spread after Geuze: {spread}.")
        return spread


RollPass.plugin_manager.add_hookspecs(Specs())
RollPass.plugin_manager.register(Impls())
