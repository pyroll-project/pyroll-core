from .transport import Transport


@Transport.OutProfile.strain
def out_strain(self: Transport.OutProfile):
    """Assume total recrystallization during transport."""
    return 0


@Transport.OutProfile.velocity
def out_velocity(self: Transport.OutProfile):
    return self.transport().velocity


@Transport.velocity
def velocity(self: Transport):
    return self.in_profile.velocity


@Transport.duration
def duration(self: Transport):
    return self.length / self.velocity
