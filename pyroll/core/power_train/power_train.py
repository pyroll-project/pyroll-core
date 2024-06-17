from ..hooks import HookHost, Hook


class PowerTrain(HookHost):
    """Represents a power train."""

    torque = Hook[float]()
    """Torque of the power train."""

    power = Hook[float]()
    """Power output of the power train."""

    rotational_frequency = Hook[float]()
    """Rotational frequency of the power train."""
