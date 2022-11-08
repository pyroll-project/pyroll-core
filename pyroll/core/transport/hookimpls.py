from .transport import Transport


@Transport.OutProfile.equivalent_strain
def strain(self: Transport.OutProfile):
    """Assume total recrystallization during transport."""
    return 0


@Transport.label
def label(self: Transport):
    return "Transport"
