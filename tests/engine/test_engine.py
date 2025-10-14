from pyroll.core import RollPass, Roll, CircularOvalGroove, Engine
from numpy import isclose


def test_engine_rotational_frequency():
    rp = RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(depth=8e-3, r1=6e-3, r2=40e-3),
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3,
        ),
        engine=Engine(
            gear_ratio=2,
        ),
        gap=2e-3,
    )
    assert isclose(rp.engine.rotational_frequency, 2)


def test_roll_rotational_frequency_from_engine():
    rp = RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(depth=8e-3, r1=6e-3, r2=40e-3),
            nominal_radius=160e-3,
            neutral_point=-20e-3,
        ),
        engine=Engine(
            gear_ratio=2,
            rotational_frequency=2,
        ),
        gap=2e-3,
    )
    assert isclose(rp.roll.rotational_frequency, 1)


def test_rated_power_dc_engine():
    rp = RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(depth=8e-3, r1=6e-3, r2=40e-3),
            nominal_radius=160e-3,
            neutral_point=-20e-3,
        ),
        engine=Engine(
            label=["Engine 1 - ABB","DC"],
            gear_ratio=2,
            rotational_frequency=2,
            base_rotational_frequency=10,
            maximum_power=100
        ),
        gap=2e-3,
    )
    assert isclose(rp.engine.available_power, 20)
