import logging

import pyroll.core as pr


def test_transport_length_from_roll_pass_positions():
    sequence = pr.PassSequence(
        [
            pr.RollPass(
                roll=pr.Roll(
                    groove=None,
                ),
                entry_point=-10,
                location=100,
            ),
            pr.Transport(label="transport"),
            pr.RollPass(
                roll=pr.Roll(
                    groove=None,
                ),
                entry_point=-20,
                location=200,
            ),
        ]
    )

    assert sequence["transport"].length == 80


def test_transport_length_from_roll_pass_positions_solve(caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = pr.BoxProfile(width=1, height=3, flow_stress=1)

    sequence = pr.PassSequence(
        [
            pr.RollPass(
                roll=pr.Roll(
                    groove=pr.FlatGroove(usable_width=1),
                    nominal_radius=1,
                ),
                rotation=0,
                gap=2,
                velocity=1,
                location=100,
            ),
            pr.Transport(label="transport"),
            pr.RollPass(
                roll=pr.Roll(
                    groove=pr.FlatGroove(usable_width=1),
                    nominal_radius=1,
                ),
                rotation=0,
                gap=1,
                velocity=1,
                location=200,
            ),
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print(caplog.text)

    assert sequence["transport"].length == 100 - sequence.roll_passes[1].roll.contact_length


def test_transport_length_from_roll_pass_positions_with_shadow():
    sequence = pr.PassSequence(
        [
            pr.RollPass(
                roll=pr.Roll(
                    groove=None,
                ),
                location=100,
                entry_point=-10,
            ),
            pr.Transport(length=5),
            pr.Transport(label="transport"),
            pr.Transport(length=10),
            pr.RollPass(
                roll=pr.Roll(
                    groove=None,
                ),
                location=200,
                entry_point=-20,
            ),
        ]
    )

    assert sequence["transport"].length == 65


def test_transport_length_from_roll_pass_positions_solve_with_shadow(caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = pr.BoxProfile(width=1, height=3, flow_stress=1)

    sequence = pr.PassSequence(
        [
            pr.RollPass(
                roll=pr.Roll(
                    groove=pr.FlatGroove(usable_width=1),
                    nominal_radius=1,
                ),
                rotation=0,
                gap=2,
                velocity=1,
                location=100,
            ),
            pr.Transport(length=5),
            pr.Transport(label="transport"),
            pr.Transport(length=10),
            pr.RollPass(
                roll=pr.Roll(
                    groove=pr.FlatGroove(usable_width=1),
                    nominal_radius=1,
                ),
                rotation=0,
                gap=1,
                velocity=1,
                location=200,
            ),
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print(caplog.text)

    assert sequence["transport"].length == 100 - sequence.roll_passes[1].roll.contact_length - 15
