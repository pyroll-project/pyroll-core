from importlib import reload

from pyroll.core import solve, RollPass


def test_dummy_plugin():
    import pyroll.ui.cli.res.input_min as input_py
    reload(input_py)
    import pyroll.dummy_plugin

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    RollPass.plugin_manager.unregister(pyroll.dummy_plugin)

    assert sequence[0].roll_force == 42
