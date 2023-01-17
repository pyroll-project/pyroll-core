import numpy as np

from .sequence import PassSequence


@PassSequence.total_elongation
def total_elongation(self: PassSequence):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area


@PassSequence.duration
def duration(self: PassSequence):
    return np.sum([u.duration for u in self.units])


@PassSequence.length
def length(self: PassSequence):
    return np.sum([u.length for u in self.units])
