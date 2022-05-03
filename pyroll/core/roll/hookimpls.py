from .roll import Roll


@Roll.hookimpl
def working_radius(roll: Roll):
    return roll.nominal_radius - roll.groove.cross_section.centroid.y


@Roll.hookimpl
def min_radius(roll: Roll):
    return roll.nominal_radius - roll.groove.depth


@Roll.hookimpl
def max_radius(roll: Roll):
    return roll.nominal_radius
