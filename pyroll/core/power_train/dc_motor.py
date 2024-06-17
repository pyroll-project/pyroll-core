from .power_train import PowerTrain
from ..hooks import Hook


class DCMotor(PowerTrain):
    """Represents an DC engine witch is used to drive a roll pass."""

    static_torque = Hook[float]()
    """Static torque of the engine."""

    dynamic_torque = Hook[float]()
    """Dynamic torque of the engine."""

    frictional_torque = Hook[float]()
    """Frictional torque of the engine."""

    cutout_torque = Hook[float]()
    """Max. available torque of the engine."""

    maximum_available_power = Hook[float]()
    """Max. available power output of the engine."""

    bearing_friction_coefficient = Hook[float]()
    """Coefficient of friction of the engine bearings."""

    bearing_efficiency = Hook[float]()
    """Efficiency of the used bearings."""

    gear_ratio = Hook[float]()
    """Gear ratio of the gear box of the engine."""

    base_rotational_frequency = Hook[float]()
    """The frequency in DC engines where the engine switches from anchor range to field weakening range."""

    gearbox_efficiency = Hook[float]()
    """Efficiency of the used gearbox bearings."""
