from ..roll_pass_entry import RollPassEntry
from ... import RollPass


def check_if_successor_is_roll_pass(self):
    if not isinstance(self.next, RollPass):
        raise ValueError("Unit can only follow a RollPass unit.")


@RollPassEntry.length
def length(self: RollPassEntry):
    check_if_successor_is_roll_pass(self)
    return self.prev.exit_point + self.prev.roll.nominal_radius


@RollPassEntry.duration
def duration(self: RollPassEntry):
    if self.has_set_or_cached("length"):
        return self.length / self.velocity


@RollPassEntry.velocity(
    trylast=True  # do not override getting from in_profile
)
def conti_velocity(self: RollPassEntry):
    if self.has_set_or_cached("length"):  # probably indicates conti process
        return self.prev.velocity


@RollPassEntry.environment_temperature
def environment_temperature(self: RollPassEntry):
    return 25 + 273.15


@RollPassEntry.cooling_water_temperature
def cooling_water_temperature(self: RollPassEntry):
    return 25 + 273.15
