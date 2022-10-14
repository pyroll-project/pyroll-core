import makefun

from ..core.roll_pass.roll_pass import RollPass
from ..core.profile.profile import Profile


def for_materials(*keys: str):
    """
    A decorator that wraps the hook implementation function with a check for specified material keys.
    The hook specification must have a ``profile`` argument.
    This decorator sets a ``for_materials`` attribute on the function object to remember the ``keys``.
    This decorator can be applied multiple times.

    :param keys: one or more string keys that represent materials this hook implementation should apply to
    :returns: the hook result, if one item of ``profile.material`` is in ``keys``, else ``None``
    """

    def decorator(func):
        if hasattr(func, "for_materials"):
            func.for_materials = func.for_materials.union(k.lower() for k in keys)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            profile: Profile = kwargs["profile"]
            if hasattr(profile, "material"):
                if isinstance(profile.material, str):
                    material = {profile.material.lower()}
                else:
                    material = {m.lower() for m in profile.material}
                if wrapper.for_materials.intersection(material):
                    return func(**kwargs)
            return None

        setattr(wrapper, "for_materials", {k.lower() for k in keys})

        return wrapper

    return decorator


def for_in_profile_types(*keys: str):
    """
    A decorator that wraps the hook implementation function with a check for specified incoming profile groove types.
    The hook specification must have a ``roll_pass`` argument.
    This decorator sets a ``for_in_profile_types`` attribute on the function object to remember the ``keys``.
    This decorator can be applied multiple times.

    :param keys: one or more string keys that represent the groove types of the incoming profile
        this hook implementation should apply to
    :returns: the hook result, if the value of ``roll_pass.in_profile.types`` intersects with ``keys``,
        else ``None``
    """

    def decorator(func):
        if hasattr(func, "for_in_profile_types"):
            func.for_in_profile_types = func.for_in_profile_types.union(k.lower() for k in keys)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            roll_pass: RollPass = kwargs["roll_pass"]
            if wrapper.for_in_profile_types.intersection(roll_pass.in_profile.types):
                return func(**kwargs)
            return None

        setattr(wrapper, "for_in_profile_types", {k.lower() for k in keys})

        return wrapper

    return decorator


def for_out_profile_types(*keys: str):
    """
    A decorator that wraps the hook implementation function with a check for specified outgoing profile groove types.
    The hook specification must have a ``roll_pass`` argument.
    This decorator sets a ``for_out_profile_types`` attribute on the function object to remember the ``keys``.
    This decorator can be applied multiple times.

    **Remark:** this decorator is similar to :py:func:`for_roll_pass_types` but checks for
    ``roll_pass.out_profile.types`` instead of ``roll_pass.groove.types``.
    Commonly, both should lead to the same results, as ``roll_pass.out_profile.groove``
    is set from ``roll_pass.groove``.

    :param keys: one or more string keys that represent the groove types of the outgoing profile
        this hook implementation should apply to
    :returns: the hook result, if the value of ``roll_pass.out_profile.types`` intersects with ``keys``,
        else ``None``
    """

    def decorator(func):
        if hasattr(func, "for_out_profile_types"):
            func.for_out_profile_types = func.for_out_profile_types.union(k.lower() for k in keys)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            roll_pass: RollPass = kwargs["roll_pass"]
            if wrapper.for_out_profile_types.intersection(roll_pass.out_profile.types):
                return func(**kwargs)
            return None

        setattr(wrapper, "for_out_profile_types", {k.lower() for k in keys})

        return wrapper

    return decorator


def for_roll_pass_types(*keys: str):
    """
    A decorator that wraps the hook implementation function with a check for specified outgoing profile groove types.
    The hook specification must have a ``roll_pass`` argument.
    This decorator sets a ``for_roll_pass_types`` attribute on the function object to remember the ``keys``.
    This decorator can be applied multiple times.

    **Remark:** this decorator is similar to :py:func:`for_out_profile_types` but checks for ``roll_pass.types``
    instead of ``roll_pass.out_profile.types``.
    Commonly, both should lead to the same results, as ``roll_pass.out_profile.groove``
    is set from ``roll_pass.groove``.

    :param keys: one or more string keys that represent the groove types of the outgoing profile
        this hook implementation should apply to
    :returns: the hook result, if the value of ``roll_pass.types`` intersects with ``keys``,
        else ``None``
    """

    def decorator(func):
        if hasattr(func, "for_roll_pass_types"):
            func.for_roll_pass_types = func.for_roll_pass_types.union(k.lower() for k in keys)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            roll_pass: RollPass = kwargs["roll_pass"]
            if wrapper.for_roll_pass_types.intersection(roll_pass.types):
                return func(**kwargs)
            return None

        setattr(wrapper, "for_roll_pass_types", {k.lower() for k in keys})

        return wrapper

    return decorator


def for_units(*units: type):
    """
    A decorator that wraps the hook implementation function with a check for specified units.
    The hook specification must have a ``unit`` argument.
    This decorator sets a ``for_units`` attribute on the function object to remember the ``units``.
    This decorator can be applied multiple times.

    :param units: one or more types to which this hook implementation should apply to
    :returns: the hook result, if ``unit`` is an instance of one of the ``units``, else ``None``
    """

    def decorator(func):
        if hasattr(func, "for_units"):
            func.for_units = func.for_units.union(units)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            unit = kwargs["unit"]
            for t in wrapper.for_units:
                if isinstance(unit, t):
                    return func(**kwargs)
            return None

        setattr(wrapper, "for_units", set(units))

        return wrapper

    return decorator
