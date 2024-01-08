import numpy as np

from ..roll_pass import DeformationUnit


@DeformationUnit.draught
def draught(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.height / self.in_profile.equivalent_rectangle.height


@DeformationUnit.spread
def spread(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.width / self.in_profile.equivalent_rectangle.width


@DeformationUnit.elongation
def elongation(self: DeformationUnit):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area * self.tension_elongation


@DeformationUnit.tension_elongation
def tension_elongation(self: DeformationUnit):
    return np.exp(self.log_tension_elongation)


@DeformationUnit.log_draught
def log_draught(self: DeformationUnit):
    return np.log(self.draught)


@DeformationUnit.log_spread
def log_spread(self: DeformationUnit):
    return np.log(self.spread)


@DeformationUnit.log_elongation
def log_elongation(self: DeformationUnit):
    return np.log(self.elongation) + self.log_tension_elongation


@DeformationUnit.log_tension_elongation
def log_tension_elongation(self: DeformationUnit):
    return 0


@DeformationUnit.abs_draught
def abs_draught(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.height - self.in_profile.equivalent_rectangle.height


@DeformationUnit.abs_spread
def abs_spread(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.width - self.in_profile.equivalent_rectangle.width


@DeformationUnit.abs_elongation
def abs_elongation(self: DeformationUnit):
    return self.out_profile.length - self.in_profile.length


@DeformationUnit.rel_draught
def rel_draught(self: DeformationUnit):
    return self.abs_draught / self.in_profile.equivalent_rectangle.height


@DeformationUnit.rel_spread
def rel_spread(self: DeformationUnit):
    return self.abs_spread / self.in_profile.equivalent_rectangle.width


@DeformationUnit.rel_elongation
def rel_elongation(self: DeformationUnit):
    return self.abs_elongation / self.in_profile.length


@DeformationUnit.strain
def strain(self: DeformationUnit):
    return np.sqrt(2 / 3 * (self.log_elongation ** 2 + self.log_spread ** 2 + self.log_draught ** 2))


@DeformationUnit.strain_rate
def strain_rate(self: DeformationUnit):
    return np.abs(self.strain) / self.duration


@DeformationUnit.free_surface_area
def free_surface_area(self: DeformationUnit):
    return self.surface_area - self.contact_area
