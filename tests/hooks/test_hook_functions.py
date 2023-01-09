from typing import Any

from pyroll.core import Hook, HookHost


def test_add_and_remove_functions():
    hook = Hook[Any]("hook", object)

    @hook
    def f1(self):
        return 42

    assert f1 in hook.functions

    hook.remove_function(f1)

    assert f1 not in hook.functions


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

    host.clear_hook_cache()

    assert not host.has_cached("hook1")
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

