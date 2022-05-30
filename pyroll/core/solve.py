from typing import Iterable

from .profile import Profile
from .unit import Unit


def solve(unit_sequence: Iterable[Unit], in_profile: Profile):
    last_profile = in_profile
    for u in unit_sequence:
        try:
            last_profile = u.solve(last_profile)
        except Exception as e:
            raise RuntimeError(f"Solution of pass sequence failed at unit {u}.") from e
