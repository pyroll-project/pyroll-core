from .transport import Transport


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
