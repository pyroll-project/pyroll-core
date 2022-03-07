import logging
import sys

import numpy as np

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
    def width_change(roll_pass: RollPass):
        """
        Geuze spreading model: Δb = c * Δh


        Parameters
        ----------
        roll_pass

        Returns
        -------
        dict with width_change (Δb) and spreading (β)

        """
        log = logging.getLogger(__name__)

        if roll_pass.geuze_coefficient is None:
            log.warning(f"No Geuze coefficient available for {roll_pass.label}.")
            return None

        in_equivalent_height = roll_pass.in_profile.equivalent_rectangle.height
        out_equivalent_height = roll_pass.ideal_out_profile.equivalent_rectangle.height
        equivalent_height_change = in_equivalent_height - out_equivalent_height

        in_equivalent_width = roll_pass.in_profile.equivalent_rectangle.width
        out_equivalent_width = in_equivalent_width + roll_pass.geuze_coefficient * equivalent_height_change

        out_profile_width = out_equivalent_width * roll_pass.out_profile.height / out_equivalent_height
        width_change = out_profile_width - roll_pass.in_profile.rotated.width

        log.debug(f"Width change after Geuze: {width_change}.")
        return width_change


RollPass.plugin_manager.add_hookspecs(Specs())
RollPass.plugin_manager.register(Impls())
