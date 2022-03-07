from typing import Iterable

from .profile import Profile
from .unit import Unit


def solve(roll_passes: Iterable[Unit], in_profile: Profile):
    last_profile = in_profile
    for p in roll_passes:
        last_profile = p.solve(last_profile)
