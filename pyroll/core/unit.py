from typing import Optional
from .profile import Profile


class Unit:
    def __init__(self, label: str):
        self.out_profile: Optional[Profile] = None
        self.in_profile: Optional[Profile] = None
        self.label = label

    def solve(self, in_profile: Profile) -> Profile:
        raise NotImplementedError
