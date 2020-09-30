import math

from pytest import raises

from farey.algo import find_rational_approximation
from farey.data import Rational
from farey.tests import assert_almost_equal


def test_input():
    x = 0.5
    with raises(ValueError) as excinfo:
        _ = find_rational_approximation(x, method="farey")
    assert str(excinfo.value) == "must specify one of places or max_denominator"

    with raises(ValueError) as excinfo:
        _ = find_rational_approximation(x, method="my own")
    assert str(excinfo.value) == "method should be one of ['farey']"


def test_rational_approximation_of_irrational():
    x = math.sqrt(2) - 1  # 0.41421356237309515
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(2378, 5741)
    assert_almost_equal(x, float(r), places=7)

    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(408, 985)


def test_rational_approximation_of_rational():
    x = 0.5
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(1, 2)
    assert_almost_equal(x, float(r), places=7)

    x = 0.4
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(2, 5)
    assert_almost_equal(x, float(r), places=7)

    x = 0.5
    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(1, 2)

    x = 0.4
    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(2, 5)


def test_rational_approximation_zero():
    x = 0
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(0, 1)


def test_rational_approximation_less_than_zero():
    x = 1 - math.sqrt(3)  # -0.7320508075688772
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(-2131, 2911)
    assert_almost_equal(x, float(r), places=7)

    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(-571, 780)


def test_rational_approximation_between_half_and_one():
    x = math.sqrt(3) - 1  # 0.7320508075688772
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(2131, 2911)
    assert_almost_equal(x, float(r), places=7)

    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(571, 780)


def test_rational_approximation_greater_than_one():
    x = math.sqrt(17)  # 4.123105625617661
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(17684, 4289)
    assert_almost_equal(x, float(r), places=7)

    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(2177, 528)


def test_rational_approximation_extremal():
    x = 0.000000001
    r = find_rational_approximation(x, method="farey", places=7)
    assert r == Rational(0, 1)
    assert_almost_equal(x, float(r), places=7)

    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(0, 1)

    x = 0.0009
    r = find_rational_approximation(x, method="farey", max_denominator=1000)
    assert r == Rational(1, 1000)
