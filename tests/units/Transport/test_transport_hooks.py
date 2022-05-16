import pytest

from pyroll.core import Transport


class Specs:
    @Transport.hookspec
    def hook1(self, transport):
        """"""


Transport.plugin_manager.add_hookspecs(Specs())


def test_hook_not_present():
    transport = Transport(time=1)

    with pytest.raises(AttributeError):
        print(transport.does_not_exist)


def test_hook_result_none():
    transport = Transport(time=1)

    with pytest.raises(AttributeError):
        print(transport.hook1)
