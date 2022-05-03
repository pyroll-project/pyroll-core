from ..transport import Transport


@Transport.OutProfile.hookspec
def strain(transport: Transport, profile: Transport.OutProfile) -> float:
    """The equivalent strain of the outgoing profile of the transport unit."""
