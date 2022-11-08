from .transport import Transport


@Transport.OutProfile.strain
def strain(self: Transport.OutProfile):
    """Assume total recrystallization during transport."""
    return 0


@Transport.label
def label(self: Transport):
    return "Transport"


@Transport.velocity
def velocity(self: Transport):
    return self.in_profile.velocity


@Transport.duration
def duration(self: Transport):
    return self.length / self.velocity
