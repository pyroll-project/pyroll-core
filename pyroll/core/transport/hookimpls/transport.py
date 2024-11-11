from ..transport import Transport


@Transport.OutProfile.strain
def out_strain(self: Transport.OutProfile):
    """Assume total recrystallization during transport."""
    return 0


@Transport.duration
def duration(self: Transport):
    if self.has_set_or_cached("length"):
        return self.length / self.velocity


@Transport.velocity(
    trylast=True  # do not override getting from in_profile
)
def conti_velocity(self: Transport):
    if self.has_set_or_cached("length"):  # probably indicates conti process
        return self.prev.velocity


@Transport.environment_temperature
def environment_temperature(self):
    return 293


@Transport.length
def length_from_roll_pass_positions(self: Transport, cycle):
    if cycle:
        return None

    from pyroll.core import RollPass
    next_pass = self.next_of(RollPass)
    prev_pass = self.prev_of(RollPass)

    if next_pass.has_value("location") and prev_pass.has_value("location"):
        entry = next_pass.entry_point if next_pass.has_value("entry_point") else 0
        length = 0

        current = self
        while not (current.next is next_pass):
            length += current.next.length
            current = current.next

        current = self
        while not (current.prev is prev_pass):
            length += current.prev.length
            current = current.prev

        return next_pass.location - prev_pass.location + entry - length
