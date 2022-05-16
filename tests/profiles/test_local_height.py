import numpy as np

from pyroll.core import Profile


def test_local_height():
    p = Profile.diamond(10, 20, 2)

    fun = np.vectorize(p.local_height)

    h: np.ndarray = fun(np.linspace(-11, 11, 20))

    print()
    print(h)

    assert np.isclose(h - h[::-1], 0).all()
    assert (h >= 0).all()
    assert (h <= p.height).all()


def test_local_width():
    p = Profile.diamond(10, 20, 2)

    fun = np.vectorize(p.local_width)

    w: np.ndarray = fun(np.linspace(-6, 6, 20))

    print()
    print(w)

    assert np.isclose(w - w[::-1], 0).all()
    assert (w >= 0).all()
    assert (w <= p.width).all()
