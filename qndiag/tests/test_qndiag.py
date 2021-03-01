import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_raises

from qndiag import qndiag


@pytest.mark.parametrize('weights', [None, True])
def test_qndiag(weights):
    n, p = 10, 3
    rng = np.random.RandomState(42)
    diagonals = rng.uniform(size=(n, p))
    A = rng.randn(p, p)  # mixing matrix
    C = np.array([A.dot(d[:, None] * A.T) for d in diagonals])  # dataset
    if weights:
        weights = rng.rand(n)
    B, _ = qndiag(C, weights=weights)  # use the algorithm
    BA = np.abs(B.dot(A))  # BA Should be a permutation + scale matrix
    BA /= np.max(BA, axis=1, keepdims=True)
    BA[np.abs(BA) < 1e-8] = 0.
    assert_array_equal(BA[np.lexsort(BA)], np.eye(p))


def test_errors():
    n, p = 10, 2
    rng = np.random.RandomState(42)
    with assert_raises(ValueError):
        x = rng.randn(n, p)
        qndiag(x)
    with assert_raises(ValueError):
        x = rng.randn(n, p, p + 1)
        qndiag(x)
    with assert_raises(ValueError):
        x = rng.randn(n, p, p)
        qndiag(x)
    with assert_raises(ValueError):
        x = rng.randn(n, p, p)
        x += x.swapaxes(1, 2)
        x[0] = np.array([[0, 1], [1, 0]])
        qndiag(x)
