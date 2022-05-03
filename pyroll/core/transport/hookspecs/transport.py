from ..transport import Transport


@Transport.hookspec
def duration(transport: Transport) -> float:
    """Duration of the transport."""
