import math

from farey.algo import find_rational_approximation
from farey.data import Rational
from tests import assert_almost_equal


def test_rational_approximation_of_irrational():
    x = math.sqrt(2) - 1
    r = find_rational_approximation(x, places=7)
    assert r == Rational(2378, 5741)
    assert_almost_equal(x, float(r), places=7)


def test_rational_approximation_of_rational():
    x = 0.5
    r = find_rational_approximation(x, places=7)
    assert r == Rational(1, 2)
    assert_almost_equal(x, float(r), places=7)


def test_rational_approximation_less_than_zero():
    x = 1 - math.sqrt(3)
    r = find_rational_approximation(x, places=7)
    assert r == Rational(-2131, 2911)
    assert_almost_equal(x, float(r), places=7)


def test_rational_approximation_greater_than_one():
    x = math.sqrt(17)
    r = find_rational_approximation(x, places=7)
    assert r == Rational(17684, 4289)
    assert_almost_equal(x, float(r), places=7)
