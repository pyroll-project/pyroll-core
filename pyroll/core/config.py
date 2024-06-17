import os
from pathlib import Path
from typing import Optional, Iterable, Mapping, Any, Callable


class ConfigValue:
    """Helper descriptor for storing configuration values, able to determine the value from explictly set values,
     environment variables and default values."""

    def __init__(
            self,
            default,
            *,
            env_var: Optional[str] = None,
            env_var_prefix: Optional[str] = None,
            parser: Optional[Callable[[str], Any]] = None
    ):
        self.default = default
        self.type = type(default)
        self.parser = parser

        self._env_var = env_var
        self._env_var_prefix = env_var_prefix

    def __set_name__(self, owner: type, name: str):
        self.owner = owner
        self.name = name
        if not self._env_var_prefix:
            self._env_var_prefix = self.owner.__module__.upper().replace('.', '_')

    @property
    def env_var(self):
        """The name of the related environment variable."""
        if self._env_var:
            return self._env_var

        return f"{self._env_var_prefix}_{self.name.upper()}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = getattr(instance, "_" + self.name, None)

        if value is not None:
            return value

        value = os.getenv(self.env_var, None)

        if value is not None:
            return self._parse(value)

        return self.default

    def __set__(self, instance, value):
        setattr(instance, "_" + self.name, value)

    def __delete__(self, instance):
        delattr(instance, "_" + self.name)

    def _parse(self, s: str):
        """Parse value from string."""
        if self.parser:
            return self.parser(s)
        if self.type is bool:
            if s.lower().strip() == "true":
                return True
            elif s.lower().strip() == "false":
                return False
            raise ValueError(f"{s} could not be parsed to bool")
        if self.type is Path:
            return Path(s)
        if self.type is str:
            return s
        if issubclass(self.type, Mapping):
            return self.type((p2.strip() for p2 in p.strip().split("=")) for p in s.split(","))
        if issubclass(self.type, Iterable):
            return self.type(p.strip() for p in s.split(","))

        return self.type(s)


class ConfigMeta(type):
    def to_dict(cls):
        """Return the config values of this class as dict."""
        return {
            n: v
            for n, v in type(cls).__dict__.items()
            if isinstance(v, ConfigValue)
        }

    def update(cls, d: dict[str, Any]):
        """
        Update the config values of this class from a dict.

        :return: the updated contents
        """
        for n, v in d.items():
            cv = type(cls).__dict__.get(n, None)
            if isinstance(cv, ConfigValue):
                setattr(cls, n, v)
            else:
                AttributeError(f"{cls} has no config value {n}")

        return cls.to_dict()


def config(env_var_prefix):
    """
    Decorator for creating config classes.
    Automatically creates a metaclass with respective :py:class:`ConfigValue` descriptors for class attributes with
    uppercase names that do not start with underscore.

    Use it as follows::

        @config("PREFIX")
        class Config:
            VAR1 = 42
            VAR2 = "abc"

            # not modified
            _PRIV_VAR = None
            normal_var = None


    :param env_var_prefix: prefix for the respective env vars, should be uppercase and delimited by underscores
    """

    def dec(cls):
        meta_dict = {}
        cls_dict = dict(cls.__dict__)

        for n, v in cls.__dict__.items():
            if n.isupper() and not n.startswith("_"):
                del cls_dict[n]
                if not isinstance(v, ConfigValue):
                    meta_dict[n] = ConfigValue(default=v, env_var_prefix=env_var_prefix)
                else:
                    # noinspection PyProtectedMember
                    meta_dict[n] = ConfigValue(
                        default=v.default,
                        env_var_prefix=env_var_prefix,
                        env_var=v._env_var,
                        parser=v.parser
                    )

        meta = type(cls.__name__ + "Meta", (ConfigMeta,), meta_dict)
        cls = meta(cls.__name__, cls.__bases__, cls_dict)
        return cls

    return dec


@config("PYROLL_CORE")
class Config:
    """Configuration class for ``pyroll.core``."""
    ROLL_PASS_AUTO_ROTATION = True
    """Whether to enable automatic rotation of incoming profiles in roll passes by default."""

    GROOVE_PADDING = 0.2
    """Fraction of the total groove width that is added at the sides of the groove contour to represent the roll face."""

    DEFAULT_MAX_ITERATION_COUNT = 100
    """Default maximum count of iterations before aborting the loop."""

    DEFAULT_ITERATION_PRECISION = 1e-3
    """Default precision of iteration loops required to break successfully."""

    ROLL_SURFACE_DISCRETIZATION_COUNT = 100
    """Count of discrete points used to describe the roll surface."""

    UNIVERSAL_GAS_CONSTANT = 8.31446261815324
    """Universal gas constant R."""

    BOLTZMANN_CONSTANT = 1.380649e-23
    """Boltzmann constant kB."""

    STEFAN_BOLTZMANN_CONSTANT = 5.670374419e-8
    """Stefan-Boltzmann radiation constant σ."""

    AVOGADRO_CONSTANT = 6.02214076e23
    """Avogadro constant NA."""

    STANDARD_GRAVITY = 9.80665
    """Standard acceleration of gravity g0."""

    PROFILE_CONTOUR_REFINEMENT = 0
    """Refine the line string of profile contours with more intermediate points. 
    Higher integers mean finer. Values < 1 disable this feature."""

    GROOVE_RADIUS_POINT_COUNT = 20
    """Count of points used to represent the radii in a generic elongation groove as line string."""

    PLOT_WIDTH = 640
    """Width of plots (using ReprMixin) in pixels."""

    PLOT_HEIGHT = 480
    """Height of plots (using ReprMixin) in pixels."""

    PLOT_RESOLUTION = 100
    """Resolution of plots in dots per inches (dpi)."""
