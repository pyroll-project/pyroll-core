import numpy as np

from .sequence import PassSequence


@PassSequence.elongation
def total_elongation(self: PassSequence):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area


@PassSequence.log_elongation
def total_log_elongation(self: PassSequence):
    return np.log(self.elongation)


@PassSequence.abs_elongation
def total_abs_elongation(self: PassSequence):
    return self.out_profile.length - self.in_profile.length


@PassSequence.rel_elongation
def total_rel_elongation(self: PassSequence):
    return self.abs_elongation / self.in_profile.length


@PassSequence.duration
def duration(self: PassSequence):
    return np.sum([u.duration for u in self.units])


@PassSequence.length
def length(self: PassSequence):
    return np.sum([u.length for u in self.units])
