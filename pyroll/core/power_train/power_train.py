from ..hooks import HookHost, Hook


class PowerTrain(HookHost):
    """Represents a power train."""

    torque = Hook[float]()
    """Torque of the power train."""

    power = Hook[float]()
    """Power output of the engine."""

    rotational_frequency = Hook[float]()
    """Rotational frequency of the engine."""

    def __init__(
            self,

            **kwargs
    ):
        """
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """
        self.__dict__.update(kwargs)

        super().__init__()

    def reevaluate_cache(self):
        super().reevaluate_cache()
