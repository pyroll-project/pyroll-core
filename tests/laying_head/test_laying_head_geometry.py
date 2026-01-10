import logging

from matplotlib import pyplot as plt

import pyroll.core as pr


def test_laying_head_coil_geometry_visual(caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    in_profile = pr.RoundProfile(diameter=5e-3, length=15, velocity=100, flow_stress=1)

    sequence = pr.PassSequence(
        [
            pr.LayingHead(
                winding_diameter=1007e-3,
                stelmor_conveyor_velocity=0.6
            )
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print(caplog.text)

    laying_head = sequence[-1]

    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    axes[0].grid(True)
    axes[0].set_title("Conveyor Belt Top View")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].plot(laying_head.stelmor_layer_distribution[0], laying_head.stelmor_layer_distribution[1])

    axes[1].grid(True)
    axes[1].set_title("Conveyor Belt Side View")
    axes[1].set_xlabel("z")
    axes[1].set_ylabel("y")
    axes[1].plot(laying_head.stelmor_layer_distribution[1], laying_head.stelmor_layer_distribution[2])
    fig.show()

    axes[2].grid(True)
    axes[2].set_title("Conveyor Belt Front View")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("z")
    axes[2].plot(laying_head.stelmor_layer_distribution[0], laying_head.stelmor_layer_distribution[2])
    fig.show()

    positions = laying_head.stelmor_layer_distribution[0]
    mask = positions > 0
    x = positions[mask]

    fig2, axes2 = plt.subplots(1, 3, figsize=(12, 5))
    axes2[0].grid(True)
    axes2[0].set_title("Wire Mass Distribution Funktion")
    axes2[0].set_xlabel("x")
    axes2[0].set_ylabel(r"$\Phi(x)$ $\left[\frac{1}{m}\right]$ ")
    axes2[0].plot(x, laying_head.layer_mass_distribution)

    axes2[1].grid(True)
    axes2[1].set_title("Void Ratio")
    axes2[1].set_xlabel("x")
    axes2[1].set_ylabel(r"$\Psi$")
    axes2[1].plot(x, laying_head.void_ratio)

    axes2[2].grid(True)
    axes2[2].set_title("Wire Horizontal Distance")
    axes2[2].set_xlabel("x")
    axes2[2].set_ylabel("s")
    axes2[2].plot(x, laying_head.layer_horizontal_distance)
    fig2.show()
