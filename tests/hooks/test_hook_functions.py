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