from . import shapes as _

from .grooves import *
from .transport import Transport, CoolingPipe
from .roll_pass import RollPass, DeformationUnit, ThreeRollPass
from .unit import Unit
from .roll import Roll
from .profile import *
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit
from .config import Config, config

VERSION = "2.1.8"

root_hooks.extend(
    [
        RollPass.roll_force,
        RollPass.Roll.roll_torque,
        RollPass.elongation_efficiency,
        Unit.power,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.classifiers,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.t,
        RollPass.OutProfile.filling_ratio,
        RollPass.OutProfile.cross_section_filling_ratio,
        RollPass.OutProfile.filling_error,
        RollPass.OutProfile.cross_section_error,
        RollPass.OutProfile.velocity,
        PassSequence.log_elongation,
    ]
)

# determine available plotting backend, plotly is preferred

import platform

try:
    import plotly as _
    PLOTTING_BACKEND = "plotly"

    try:
        import kaleido
        try:
            if platform.system() == 'Windows':
                if kaleido.__version__ != '0.1.0.post1':
                    raise ValueError("Kaleido Version 0.1.0.post1 is required to use plotly on Windows machines")
        except AttributeError:
            pass
    except ImportError:
        print("The kaleido package is required if plotly is to be used")

except ImportError:
    try:
        import matplotlib as _
        PLOTTING_BACKEND = "matplotlib"

    except ImportError:
        PLOTTING_BACKEND = None
