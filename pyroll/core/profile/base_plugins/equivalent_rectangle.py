import numpy as np

from ..profile import Profile
from ...shapes import rectangle, Polygon


@Profile.hookimpl
def equivalent_rectangle(profile: Profile):
    width = profile.width
    height = profile.height

    eq_width = np.sqrt(profile.cross_section.area * width / height)
    eq_height = np.sqrt(profile.cross_section.area * height / width)

    return rectangle(eq_width, eq_height)


@Profile.hookimpl(
    specname="equivalent_rectangle",
    hookwrapper=True
)
def equivalent_rectangle_enforce_polygon_type():
    result = yield

    result.force_result(Polygon(result.get_result()))
