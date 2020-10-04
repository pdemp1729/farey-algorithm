import math

from pytest import raises

from farey.algo import ALLOWED_METHODS, best_rational_approximation
from farey.data import Rational
from farey.tests import assert_almost_equal


def test_input():
    x = 0.5
    with raises(ValueError) as excinfo:
        _ = best_rational_approximation(x, method="farey")
    assert str(excinfo.value) == "must specify one of places or max_denominator"

    with raises(ValueError) as excinfo:
        _ = best_rational_approximation(x, method="continued_fraction")
    assert str(excinfo.value) == "must specify one of places or max_denominator"

    with raises(ValueError) as excinfo:
        _ = best_rational_approximation(x, method="my own")
    assert (
        str(excinfo.value) == "method should be one of ['farey', 'continued_fraction']"
    )


def test_rational_approximation_of_irrational():
    x = math.sqrt(2) - 1  # 0.41421356237309515
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(2378, 5741)
        assert_almost_equal(x, float(r), places=7)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(408, 985)


def test_rational_approximation_of_rational():
    x = 0.5
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(1, 2)
        assert_almost_equal(x, float(r), places=7)

    x = 0.4
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(2, 5)
        assert_almost_equal(x, float(r), places=7)

    x = 0.5
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(1, 2)

    x = 0.4
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(2, 5)


def test_rational_approximation_zero():
    x = 0
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(0, 1)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=10)
        assert r == Rational(0, 1)


def test_rational_approximation_less_than_zero():
    x = 1 - math.sqrt(3)  # -0.7320508075688772
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(-2131, 2911)
        assert_almost_equal(x, float(r), places=7)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(-571, 780)


def test_rational_approximation_between_half_and_one():
    x = math.sqrt(3) - 1  # 0.7320508075688772
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(2131, 2911)
        assert_almost_equal(x, float(r), places=7)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(571, 780)


def test_rational_approximation_greater_than_one():
    x = math.sqrt(17)  # 4.123105625617661
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(17684, 4289)
        assert_almost_equal(x, float(r), places=7)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(2177, 528)


def test_rational_approximation_extremal():
    x = 0.000000001
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, places=7)
        assert r == Rational(0, 1)
        assert_almost_equal(x, float(r), places=7)

    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(0, 1)

    x = 0.0009
    for method in ALLOWED_METHODS:
        r = best_rational_approximation(x, method=method, max_denominator=1000)
        assert r == Rational(1, 1000)


def test_continued_fraction_method_full_coverage():
    x = math.sqrt(2)
    r1 = best_rational_approximation(
        x, method="continued_fraction", max_denominator=100
    )
    # truncating at n=5 -> [1; 2, 2, 2, 2, 2] = 99/70
    # truncating at n=6 -> [1; 2, 2, 2, 2, 2, 2] = 239/169, so we have gone too far, and have
    # to check reducing the latter continued fraction, checking [1; 2, 2, 2, 2, 2, 1] = 140/99
    # since the denominator is now < max_denominator, and the last_value is even,
    # we have to check the error:
    # abs(x - 140/99) ~ 7.214 * 10^-5 vs. abs(x - 99/70) ~ 7.215 * 10^-5
    # which means that 140/99 is our best approximation.
    assert r1 == Rational(140, 99)

    r2 = best_rational_approximation(x, method="continued_fraction", max_denominator=10)
    # truncating at n=2 -> [1; 2, 2] = 7/5
    # truncating at n=3 -> [1; 2, 2, 2] = 17/12, so we have gone too far, and have to check
    # reducing the latter continued fraction, which gives [1; 2, 2, 1] = 10/7
    # since the denominator is now < max_denominator, and the last_value is even, we check the error:
    # abs(x - 10/7) ~ 0.01435 vs. abs(x - 7/5) ~ 0.01423
    # which means that 7/5 is our best approximation.
    assert r2 == Rational(7, 5)

    x = math.log(3)
    r3 = best_rational_approximation(x, method="continued_fraction", max_denominator=50)
    # truncating at n=1 -> [1; 10] = 11/10
    # truncating at n=2 -> [1; 10, 7] = 78/71, so we have gone too far and have to check
    # reducing the latter continued fraction, checking [1; 10, 6] down to [1; 10, 4]
    # indeed [1; 10, 6] = 67/61, [1; 10, 5] = 56/51, [1; 10, 4] = 45/41
    # since the last value is odd, we don't need to check the error so 45/41 is our best approx.
    assert r3 == Rational(45, 41)
