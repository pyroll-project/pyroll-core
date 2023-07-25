from typing import Any

import pytest

from pyroll.core import Hook, HookHost


def test_add_and_remove_functions():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1
    def f1(self):
        return 42

    assert f1 in Host.hook1.functions

    Host.hook1.remove_function(f1)

    assert f1 not in Host.hook1.functions


def test_calling():
    class Host(HookHost):
        hook1 = Hook[Any]()
        hook2 = Hook[Any]()

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook2
    def f2(self: Host):
        return self.hook1 * 2

    host = Host()

    assert host.hook1 == 21
    assert host.hook2 == 42


def test_call_order():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1
    def f2(self: Host):
        return 42

    host = Host()

    assert host.hook1 == 42


def test_call_derived():
    class Host(HookHost):
        hook1 = Hook[Any]()

    class Host2(Host):
        pass

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host2.hook1
    def f2(self: Host):
        return 42

    host = Host()
    assert host.hook1 == 21

    host2 = Host2()
    assert host2.hook1 == 42


def test_call_cycle():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1
    def f2(self: Host, cycle):
        if not cycle:
            return self.hook1 * 2

    host = Host()
    assert host.hook1 == 42


def test_cache():
    class Host(HookHost):
        hook1 = Hook[Any]()

    host = Host()

    @Host.hook1
    def f1(self: Host):
        return 21

    assert host.hook1 == 21

    @Host.hook1
    def f2(self: Host):
        return 42

    assert host.hook1 == 21
    assert host.has_cached("hook1")

    host.reevaluate_cache()

    assert host.hook1 == 42


def test_has_value():
    class Host(HookHost):
        hook1 = Hook[Any]()

    host = Host()
    assert not host.has_value("hook1")

    @Host.hook1
    def f1(self: Host):
        return 21

    assert host.has_value("hook1")
    assert not host.has_set("hook1")
    assert host.has_set_or_cached("hook1")
    assert host.hook1 == 21

    host.hook1 = 42

    assert host.has_value("hook1")
    assert host.has_set("hook1")
    assert host.has_set_or_cached("hook1")
    assert host.hook1 == 42

    del host.hook1

    assert host.has_value("hook1")
    assert not host.has_set("hook1")
    assert host.has_set_or_cached("hook1")
    assert host.hook1 == 21


def test_tryfirst_and_trylast():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1(tryfirst=True)
    def ff1(self: Host):
        return 21

    @Host.hook1(tryfirst=True)
    def ff2(self: Host):
        return 42

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1
    def f2(self: Host):
        return 42

    @Host.hook1(trylast=True)
    def fl1(self: Host):
        return 21

    @Host.hook1(trylast=True)
    def fl2(self: Host):
        return 42

    assert Host.hook1.functions == [
        ff2, ff1, f2, f1, fl2, fl1
    ]


def test_tryfirst_and_trylast_inherited():
    class Host(HookHost):
        hook1 = Hook[Any]()

    class Host2(Host):
        pass

    @Host2.hook1(tryfirst=True)
    def ff12(self: Host2):
        return 21

    @Host2.hook1(tryfirst=True)
    def ff22(self: Host2):
        return 42

    @Host2.hook1
    def f12(self: Host2):
        return 21

    @Host2.hook1
    def f22(self: Host2):
        return 42

    @Host2.hook1(trylast=True)
    def fl12(self: Host2):
        return 21

    @Host2.hook1(trylast=True)
    def fl22(self: Host2):
        return 42

    @Host.hook1(tryfirst=True)
    def ff1(self: Host):
        return 21

    @Host.hook1(tryfirst=True)
    def ff2(self: Host):
        return 42

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1
    def f2(self: Host):
        return 42

    @Host.hook1(trylast=True)
    def fl1(self: Host):
        return 21

    @Host.hook1(trylast=True)
    def fl2(self: Host):
        return 42

    assert Host.hook1.functions == [
        ff2, ff1, f2, f1, fl2, fl1
    ]

    assert Host2.hook1.functions == [
        ff22, ff12, ff2, ff1, f22, f12, f2, f1, fl22, fl12, fl2, fl1
    ]


def test_context_manager():
    class Host(HookHost):
        hook1 = Hook[Any]()

    host = Host()

    @Host.hook1
    def f1(self: Host):
        return 21

    def f2(self):
        return 42

    with Host.hook1(f2):
        assert host.hook1 == 42

    host.__cache__.clear()
    assert host.hook1 == 21


def test_wrapper():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1(wrapper=True)
    def f1(self: Host, cycle):
        if cycle:
            return None

        return 2 * (yield)

    host = Host()
    assert host.hook1 == 42


def test_wrapper_2yield():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1
    def f1(self: Host):
        return 21

    @Host.hook1(wrapper=True)
    def f1(self: Host, cycle):
        if cycle:
            return None
        b = (yield)
        return 2 * (yield)

    host = Host()

    with pytest.raises(SyntaxError):
        _ = host.hook1


def test_wrapper_none():
    class Host(HookHost):
        hook1 = Hook[Any]()

    @Host.hook1(wrapper=True)
    def f1(self: Host, cycle):
        if cycle:
            return None

        return (yield) is None

    host = Host()
    assert host.hook1
