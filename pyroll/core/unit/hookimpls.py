from .unit import Unit


@Unit.profiles
def one_step_profiles(self: Unit):
    return [self.in_profile, self.out_profile]
