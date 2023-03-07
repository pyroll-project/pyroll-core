import os
from typing import Optional


class ConfigValue:
    def __init__(self, default=None, env_var: Optional[str] = None, env_var_prefix: Optional[str] = None):
        self.default = default

        self._env_var = env_var
        self._env_var_prefix = env_var_prefix

    def __set_name__(self, owner: type, name: str):
        self.owner = owner
        self.name = name
        if not self._env_var_prefix:
            self._env_var_prefix = self.owner.__module__.upper().replace('.', '_')

    @property
    def env_var(self):
        if self._env_var:
            return self._env_var

        return f"{self._env_var_prefix}_{self.name.upper()}"

    def __get__(self, instance, owner):
        value = getattr(instance, "_" + self.name, None)

        if value is not None:
            return value

        value = os.getenv(self.env_var, None)

        if value is not None:
            return value

        return self.default

    def __set__(self, instance, value):
        setattr(instance, "_" + self.name, value)

    def __delete__(self, instance):
        delattr(instance, "_" + self.name)


def config(env_var_prefix):
    def dec(cls):
        cls_dict = {}

        for n, v in cls.__dict__.items():
            if not isinstance(v, ConfigValue):
                cls_dict[n] = ConfigValue(default=v, env_var_prefix=env_var_prefix)
            else:
                cls_dict[n] = ConfigValue(default=v.default, env_var_prefix=env_var_prefix)

        cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)
        return cls()

    return dec


@config("PYROLL_CORE")
class Config:
    ROLL_PASS_AUTO_ROTATION = True
    """Whether to enable automatic rotation of incoming profiles in roll passes by default."""

    GROOVE_PADDING = 0.2
    """Fraction of the total groove width that is added at the sides of the groove contour to represent the roll face."""

    DEFAULT_MAX_ITERATION_COUNT = 100
    """Default maximum count of iterations before aborting the loop."""

    DEFAULT_ITERATION_PRECISION = 1e-2
    """Default precision of iteration loops required to break successfully."""

    ROLL_SURFACE_DISCRETIZATION_COUNT = 100
    """Count of discrete points used to describe the roll surface."""
