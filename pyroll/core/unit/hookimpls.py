from .unit import Unit

for h in Unit.OutProfile.__hooks__:
    @getattr(Unit.OutProfile, h)
    def copy_from_in_profile(self: Unit.OutProfile, hook=h):
        return getattr(self.unit().in_profile, hook, None)


    @getattr(Unit.OutProfile, h)
    def copy_from_last_subunit(self: Unit.OutProfile, hook=h):
        if self.unit().subunits:
            return getattr(self.unit().subunits[-1].out_profile, hook, None)
