from .sequence import PassSequence


@PassSequence.total_elongation
def total_elongation(self: PassSequence):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area


