from .unit import Unit
from ..hooks import Hook


@Unit.intermediate_profile_count
def one_step(self: Unit):
    return 0


@Unit.profiles
def one_step_profiles(self: Unit):
    return [self.in_profile, self.out_profile]


for h in Unit.OutProfile.__hooks__:
    @getattr(Unit.OutProfile, h)
    def copy_from_last_subunit(self: Unit.OutProfile, hook=h):
        if self.unit().subunits:
            try:
                return getattr(self.unit().subunits[-1].out_profile, hook)
            except AttributeError:
                return None
