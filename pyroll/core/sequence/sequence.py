import copy

import numpy as np

from collections.abc import Sequence
from typing import overload, List, cast

from ..unit import Unit
from ..roll_pass import BaseRollPass
from ..transport import Transport
from ..hooks import Hook

__all__ = ["PassSequence"]


class PassSequence(Unit, Sequence[Unit]):
    """
    Represents a sequence of other units.
    Main container for defining rolling processes.
    Can be nested to define distinct rolling lines or similar.
    """

    elongation = Hook[float]()
    """Coefficient of elongation (change in length)."""

    log_elongation = Hook[float]()
    """Log. coefficient of elongation (change in length)."""

    abs_elongation = Hook[float]()
    """Absolute elongation (change in length)."""

    rel_elongation = Hook[float]()
    """Relative elongation (change in length)."""

    def __init__(self, units: Sequence[Unit], label: str = "", **kwargs):
        """
        :param units: sequence of unit objects
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label=label)
        self.__dict__.update(kwargs)
        self._subunits = self._SubUnitsList(self, units)

    class Profile(Unit.Profile):
        """Represents a profile in context of a pass sequence unit."""

        @property
        def pass_sequence(self) -> "PassSequence":
            """Reference to the pass sequence. Alias for ``self.unit``."""
            return cast(PassSequence, self.unit)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a pass sequence unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a pass sequence unit."""

    def __len__(self) -> int:
        return self._subunits.__len__()

    def __iter__(self):
        return self._subunits.__iter__()

    @overload
    def __getitem__(self, key: int) -> Unit:
        """Gets unit item by index."""
        ...

    @overload
    def __getitem__(self, key: str) -> Unit:
        """Gets unit item by label."""
        ...

    @overload
    def __getitem__(self, key: slice) -> list[Unit]:
        """Gets a slice of units."""
        ...

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return next(u for u in self._subunits if u.label == key)
            except StopIteration:
                raise KeyError(f"No unit with label '{key}' found.")

        if isinstance(key, int) or isinstance(key, slice):
            return self._subunits.__getitem__(key)

        raise TypeError("Key must be int, slice or str")

    def prepend(self, unit: Unit) -> None:
        """Prepend a unit to the beginning of the sequence."""
        self._subunits.insert(0, unit)

    def append(self, unit: Unit) -> None:
        """Append a unit to the end of the sequence."""
        self._subunits.append(unit)

    def drop(self, index: int) -> None:
        """Remove the unit at the specified index from the sequence."""
        del self._subunits[index]

    def flatten(self) -> None:
        """Flatten the sequence."""
        new_list = []
        for item in self:
            if isinstance(item, PassSequence):
                for subitem in item:
                    new_list.append(subitem)
            else:
                new_list.append(item)

        del self._subunits
        self._subunits = new_list

    @property
    def units(self) -> List[Unit]:
        """Returns a list of all units in this sequence."""
        return list(self._subunits)

    @property
    def roll_passes(self) -> List[BaseRollPass]:
        """Returns a list of all roll passes in this sequence."""
        return list(u for u in self._subunits if isinstance(u, BaseRollPass))

    @property
    def transports(self) -> List[Transport]:
        """Returns a list of all transports in this sequence."""
        return list(u for u in self._subunits if isinstance(u, Transport))

    @property
    def __attrs__(self):
        return super().__attrs__ | {"units": self.units}

    def _ipython_key_completions_(self):
        return [u.label for u in self._subunits]

    def solve_velocities_backward(self, in_profile: Profile, final_speed: float, final_cross_section_area: float):
        """
        Solve method, that calculates all velocities of the roll pass starting from the very last roll_pass of the sequence.

        :param in_profile: incoming profile
        :param final_speed: speed of the last stand
        :param final_cross_section_area: area of the final cross-section
        """

        copied_sequence = copy.deepcopy(self)

        def calculate_velocities_array(velocities: np.ndarray[float], cross_sections_areas: np.ndarray[float]):
            for i in range(len(cross_sections_areas) - 2, -1, -1):
                velocities[i] = velocities[i + 1] * cross_sections_areas[i + 1] / cross_sections_areas[i]

        def set_velocities_to_roll_passes(roll_passes: List[BaseRollPass], velocities: np.ndarray[float]):
            for roll_pass, velocity in zip(roll_passes, velocities):
                roll_pass.velocity = velocity

        usable_cross_section_areas = np.asarray([roll_pass.usable_cross_section.area for roll_pass in copied_sequence.roll_passes])
        initial_roll_pass_velocities = np.zeros_like(usable_cross_section_areas, dtype=float)

        initial_roll_pass_velocities[-1] = final_speed
        usable_cross_section_areas[-1] = final_cross_section_area

        calculate_velocities_array(velocities=initial_roll_pass_velocities, cross_sections_areas=usable_cross_section_areas)
        set_velocities_to_roll_passes(roll_passes=copied_sequence.roll_passes, velocities=initial_roll_pass_velocities)

        copied_sequence.solve(in_profile)

        for i in range(self.max_iteration_count):
            prior_roll_pass_velocities = np.asarray([roll_pass.velocity for roll_pass in copied_sequence.roll_passes])
            current_roll_pass_velocities = prior_roll_pass_velocities.copy()
            profile_areas = [roll_pass.out_profile.cross_section.area for roll_pass in copied_sequence.roll_passes]

            calculate_velocities_array(velocities=current_roll_pass_velocities, cross_sections_areas=profile_areas)
            set_velocities_to_roll_passes(roll_passes=copied_sequence.roll_passes, velocities=current_roll_pass_velocities)

            copied_sequence.solve(in_profile)

            difference = np.abs(prior_roll_pass_velocities - current_roll_pass_velocities)

            if np.all(difference < 0.01):
                set_velocities_to_roll_passes(roll_passes=self.roll_passes, velocities=current_roll_pass_velocities)
                self.solve(in_profile)
                break

    def solve_velocities_forward(self, in_profile: Profile, initial_speed: float):
        """
        Solve method, that calculates all velocities of the roll pass starting from the very first roll_pass of the sequence.

        :param in_profile: incoming profile
        :param initial_speed: speed of the first stand or output speed of a furnace
        :param final_cross_section_area: area of the final cross-section
        """

        copied_sequence = copy.deepcopy(self)

        def calculate_velocities_array(velocities: np.ndarray[float], cross_sections_areas: np.ndarray[float]):
            for i in range(1, len(usable_cross_section_areas)):
                velocities[i] = velocities[i - 1] * cross_sections_areas[i - 1] / cross_sections_areas[i]

        def set_velocities_to_roll_passes(roll_passes: List[BaseRollPass], velocities: np.ndarray[float]):
            for roll_pass, velocity in zip(roll_passes, velocities):
                roll_pass.velocity = velocity

        usable_cross_section_areas = np.asarray([roll_pass.usable_cross_section.area for roll_pass in copied_sequence.roll_passes])
        initial_roll_pass_velocities = np.zeros_like(usable_cross_section_areas, dtype=float)

        initial_roll_pass_velocities[0] = initial_speed * in_profile.cross_section.area / copied_sequence.roll_passes[0].usable_cross_section.area

        calculate_velocities_array(velocities=initial_roll_pass_velocities, cross_sections_areas=usable_cross_section_areas)
        set_velocities_to_roll_passes(roll_passes=copied_sequence.roll_passes, velocities=initial_roll_pass_velocities)

        copied_sequence.solve(in_profile)

        for i in range(self.max_iteration_count):
            prior_velocities = np.asarray([roll_pass.velocity for roll_pass in copied_sequence.roll_passes])
            profile_areas = [roll_pass.out_profile.cross_section.area for roll_pass in copied_sequence.roll_passes]
            roll_pass_velocities = np.zeros_like(usable_cross_section_areas, dtype=float)
            roll_pass_velocities[0] = initial_speed * in_profile.cross_section.area / profile_areas[0]

            calculate_velocities_array(velocities=roll_pass_velocities, cross_sections_areas=profile_areas)
            set_velocities_to_roll_passes(roll_passes=copied_sequence.roll_passes, velocities=roll_pass_velocities)

            copied_sequence.solve(in_profile)

            difference = np.abs(prior_velocities - roll_pass_velocities)

            if np.all(difference < 0.01):
                set_velocities_to_roll_passes(roll_passes=self.roll_passes, velocities=roll_pass_velocities)
                self.solve(in_profile)
                break

    def solve_interstand_tensions_with_given_velocity_ratios(self, in_profile: Profile,
                                                             velocity_ratios: np.ndarray[float], final_speed: float):
        """
        Solve method, that calculates the resulting tensions for given reductions.
        Further, it sets the velocities according to these reductions and the finishing speed.

        :param in_profile: incoming profile
        :param velocity_ratios: velocity_ratio per stand.
        :param final_speed: speed of the last stand
        """

        roll_pass_velocities = [final_speed]
        for ratio in reversed(velocity_ratios):
            previous_roll_pass_velocity = roll_pass_velocities[0] / ratio
            roll_pass_velocities.insert(0, previous_roll_pass_velocity)

        roll_pass_velocities = np.array(roll_pass_velocities)
        for i, roll_pass in enumerate(self.roll_passes):
            roll_pass.velocity = roll_pass_velocities[i]

        copied_sequence = copy.deepcopy(self)
        copied_sequence.solve(in_profile)

        tensions = np.zeros(len(copied_sequence.roll_passes) * 2)
        engineering_strains = (roll_pass_velocities[1:] - roll_pass_velocities[:-1]) / roll_pass_velocities[:-1]

        for index in range(1, len(self.roll_passes)):
            engineering_strain = engineering_strains[index - 1]

            tensions[2 * index - 1] = copied_sequence.roll_passes[
                                          index - 1].in_profile.elastic_modulus * engineering_strain
            tensions[2 * index] -= copied_sequence.roll_passes[
                                       index - 1].out_profile.elastic_modulus * engineering_strain

        tensions[0] = 0
        tensions[-1] = 0

        for index, roll_pass in enumerate(self.roll_passes):
            roll_pass.back_tension = tensions[2 * index]
            roll_pass.front_tension = tensions[2 * index + 1]

        self.solve(in_profile=in_profile)
