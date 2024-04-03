import pytest

import pyroll.core as pr
import matplotlib.pyplot as plt


def test_plot_profile_contact_contours():
    ip = pr.Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        material=["C45", "steel"],
        length=1,
        flow_stress=100e6
    )

    rp = pr.RollPass(
        label="Oval I",
        roll=pr.Roll(
            groove=pr.CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        gap=2e-3,

    )

    rp.solve(ip)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    for ccl in rp.out_profile.contact_contour_lines:
        plt.plot(*ccl.xy, color='C0')
    plt.show()
    plt.close()

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    for cca in rp.out_profile.contact_contour_angles:
        plt.plot(cca, color='C0')
    plt.show()
    plt.close()
