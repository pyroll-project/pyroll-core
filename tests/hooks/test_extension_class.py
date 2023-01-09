from pyroll.core import Profile, Hook


def test_extension_class():
    @Profile.extension_class
    class ProfileExtension:
        ext_hook = Hook[float]()
        """Docstring for ext_hook."""

    assert ProfileExtension is Profile
    assert hasattr(Profile, "ext_hook")
    assert ProfileExtension.ext_hook.owner is Profile

    @ProfileExtension.ext_hook
    def impl(self: Profile | ProfileExtension):
        return 42

    # noinspection PyUnresolvedReferences
    assert impl in Profile.ext_hook._functions
