from .roll import Roll


@Roll.working_radius
def working_radius(self: Roll):
    return self.nominal_radius - self.contour_line.centroid.y


@Roll.min_radius
def min_radius(self: Roll):
    return self.max_radius - self.contour_line.bounds[3]


@Roll.max_radius
def max_radius(self: Roll):
    return self.nominal_radius


@Roll.contour_line
def contour_line(self: Roll):
    return self.groove.contour_line
