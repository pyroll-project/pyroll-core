from typing import Tuple

import makefun


def applies_to_materials(*keys: str):
    """Wraps the hookimpl with a check for specified material keys, so that the hookimpl returns None if the profile has no fitting value in the material attribute or no such attribute at all.
    The hookspec must contain a profile argument."""

    def decorator(func):
        if hasattr(func, "materials"):
            func.materials = func.materials.union(k.lower() for k in keys)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            profile = kwargs["profile"]
            if hasattr(profile, "material"):
                if profile.material.lower() in wrapper.materials:
                    return func(**kwargs)
            return None

        setattr(wrapper, "materials", {k.lower() for k in keys})

        return wrapper

    return decorator


def applies_to_in_grooves(*grooves: type):
    """Wraps the hookimpl with a check for specified in profile grooves, so that the hookimpl returns None if the roll pass' in profile has no groove of one of the specified types.
    The hookspec must contain a roll_pass argument."""

    def decorator(func):
        if hasattr(func, "in_grooves"):
            func.in_grooves = func.in_grooves.union(grooves)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            roll_pass = kwargs["roll_pass"]
            for g in wrapper.in_grooves:
                if isinstance(roll_pass.in_profile.groove, g):
                    return func(**kwargs)
            return None

        setattr(wrapper, "in_grooves", set(grooves))

        return wrapper

    return decorator


def applies_to_out_grooves(*grooves: type):
    """Wraps the hookimpl with a check for specified out profile grooves, so that the hookimpl returns None if the roll pass' out profile has no groove of one of the specified types.
    The hookspec must contain a roll_pass argument."""

    def decorator(func):
        if hasattr(func, "out_grooves"):
            func.out_grooves = func.out_grooves.union(grooves)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            roll_pass = kwargs["roll_pass"]
            for g in wrapper.out_grooves:
                if isinstance(roll_pass.groove, g):
                    return func(**kwargs)
            return None

        setattr(wrapper, "out_grooves", set(grooves))

        return wrapper

    return decorator


def applies_to_unit_types(*unit_types: type):
    """Wraps the hookimpl with a check for specified unit types, so that the hookimpl returns None if the unit is not of one of the specified types.
    The hookspec must contain a unit argument."""

    def decorator(func):
        if hasattr(func, "unit_types"):
            func.unit_types = func.unit_types.union(unit_types)
            return func

        @makefun.wraps(func)
        def wrapper(**kwargs):
            unit = kwargs["unit"]
            for t in wrapper.unit_types:
                if isinstance(unit, t):
                    return func(**kwargs)
            return None

        setattr(wrapper, "unit_types", set(unit_types))

        return wrapper

    return decorator
