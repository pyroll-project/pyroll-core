import logging
from logging import getLogger
from typing import Union

from pyroll.core import Profile, Hook

_log = getLogger(__name__)


def test_extension_class(caplog):
    caplog.set_level(logging.INFO)

    @Profile.extension_class
    class ProfileExtension:
        ext_hook = Hook[float]()
        """Docstring for ext_hook."""

    assert ProfileExtension is Profile
    assert hasattr(Profile, "ext_hook")
    assert ProfileExtension.ext_hook.owner is Profile

    @ProfileExtension.ext_hook
    def impl(self: Profile):
        return 42

    # noinspection PyUnresolvedReferences
    assert impl in Profile.ext_hook._functions

    @Profile.width
    def call_test_impl(self: Union[ProfileExtension, Profile]):
        _log.info(self.classifiers)
        _log.info(self.ext_hook)
        return 21

    p = Profile.round(radius=10)
    assert p.width == 21
    assert [r for r in caplog.records if r.message == "42"]

    print(caplog.text)

    del ProfileExtension.ext_hook
    Profile.width.remove_function(call_test_impl)

    pass


def test_extension_class_derived(caplog):
    caplog.set_level(logging.INFO)

    @Profile.extension_class
    class ProfileExtension(Profile):
        ext_hook = Hook[float]()
        """Docstring for ext_hook."""

    assert ProfileExtension is Profile
    assert hasattr(Profile, "ext_hook")
    assert ProfileExtension.ext_hook.owner is Profile

    @ProfileExtension.ext_hook
    def impl(self: Profile):
        return 42

    # noinspection PyUnresolvedReferences
    assert impl in Profile.ext_hook._functions

    @Profile.width
    def call_test_impl(self: ProfileExtension):
        _log.info(self.classifiers)
        _log.info(self.ext_hook)
        return 21

    p = Profile.round(radius=10)
    assert p.width == 21
    assert [r for r in caplog.records if r.message == "42"]

    print(caplog.text)

    del ProfileExtension.ext_hook
    Profile.width.remove_function(call_test_impl)
