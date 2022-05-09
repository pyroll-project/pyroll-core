import numpy as np

from pyroll import Profile


def test_local_height():
    p = Profile.diamond(10, 20, 2)

    fun = np.vectorize(p.local_height, )

    h: np.ndarray = fun(np.linspace(-11, 11, 20))

    print()
    print(h)

    assert np.isclose(h - h[::-1], 0).all()
    assert (h >= 0).all()
