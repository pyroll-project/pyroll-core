from typing import Optional
from .profile import Profile


class Unit:
    """Base class for units in a pass sequence."""

    max_iteration_count = 100
    """Count of maximum solution loop iterations before aborting."""

    def __init__(self, label: str):
        self.in_profile: Optional[Profile] = None
        """Incoming workpiece state profile."""

        self.out_profile: Optional[Profile] = None
        """Outgoing workpiece state profile."""

        self.label = label
        """Label for human identification."""

    def solve(self, in_profile: Profile) -> Profile:
        """
        Solve the workpiece evolution within this unit based on the incoming state specified by in_profile.
        Returns the outgoing state.
        :param in_profile: incoming state profile
        """
        raise NotImplementedError
