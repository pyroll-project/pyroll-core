from .roll import Roll


@Roll.hookimpl
def working_radius(roll: Roll):
    return roll.nominal_radius - roll.contour_line.centroid.y


@Roll.hookimpl
def min_radius(roll: Roll):
    return roll.max_radius - roll.contour_line.bounds[3]


@Roll.hookimpl
def max_radius(roll: Roll):
    return roll.nominal_radius


@Roll.hookimpl
def contour_line(roll: Roll):
    return roll.groove.contour_line
