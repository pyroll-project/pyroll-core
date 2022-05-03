from .roll import Roll


@Roll.hookspec
def nominal_radius(roll):
    """Nominal radius of the roll (equal to the grooves y=0 axis)."""


@Roll.hookspec
def working_radius(roll):
    """Working radius of the roll (some kind of equivalent radius to flat rolling)."""


@Roll.hookspec
def min_radius(roll):
    """Minimal (inner) radius of the roll."""


@Roll.hookspec
def max_radius(roll):
    """Maximal (outer) radius of the roll."""


@Roll.hookspec
def rotational_frequency(roll):
    """The rotational frequency of the roll."""
