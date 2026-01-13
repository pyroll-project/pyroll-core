import numpy as np
from matplotlib import pyplot as plt

from pyroll.core import Spooler, Profile

in_profile = Profile.round(
    diameter=20e-3, flow_stress=1, velocity=100, length=5100, density=7500, elastic_modulus=8.3e10
)


def test_spooler_coil_geometry():
    in_profile_geometry = Profile.round(
        diameter=10e-3, flow_stress=1, velocity=100, length=5200, density=7500, elastic_modulus=8.3e10
    )

    sp = Spooler(
        label="Demo Spooler",
        mandrel_radius=300e-3,
        mandrel_width=800e-3,
        finished_coil_weight=3000,
        velocity=35,
    )

    sp.solve(in_profile_geometry)

    assert np.isclose(sp.windings_per_layer, 80)
    assert np.isclose(sp.finished_coil_radius, 0.5411044, rtol=1e-5)


def test_spooler_bending_stress_visual():
    sp = Spooler(
        label="Demo Spooler",
        mandrel_radius=300e-3,
        mandrel_width=800e-3,
        finished_coil_weight=3200,
        velocity=35,
    )

    sp.solve(in_profile)

    fig, ax = plt.subplots(figsize=(10, 6))

    layer_numbers = range(1, len(sp.coil_layer_bending_stresses) + 1)
    ax.plot(layer_numbers, sp.coil_layer_bending_stresses)

    ax.set_xlabel("Layer Number")
    ax.set_ylabel("Bending Stress")
    ax.set_title("Bending Stress per Layer")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def test_spooler_bending_torque_visual():
    sp = Spooler(
        label="Demo Spooler",
        mandrel_radius=300e-3,
        mandrel_width=800e-3,
        finished_coil_weight=3200,
        velocity=35,
    )

    sp.solve(in_profile)

    fig, ax = plt.subplots(figsize=(10, 6))

    layer_numbers = range(1, len(sp.coil_layer_bending_torques) + 1)
    ax.plot(layer_numbers, sp.coil_layer_bending_torques)

    ax.set_xlabel("Layer Number")
    ax.set_ylabel("Bending Torque")
    ax.set_title("Bending Torque per Layer")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def test_spooler_cumulative_torque_visual():
    sp = Spooler(
        label="Demo Spooler",
        mandrel_radius=300e-3,
        mandrel_width=800e-3,
        finished_coil_weight=3200,
        velocity=35,
    )

    sp.solve(in_profile)

    fig, ax = plt.subplots(figsize=(10, 6))

    layer_numbers = range(1, len(sp.coil_cumulative_torque) + 1)
    ax.plot(layer_numbers, sp.coil_cumulative_torque)

    ax.set_xlabel("Layer Number")
    ax.set_ylabel("Torque")
    ax.set_title("Cumulative Bending Torque per Layer")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
