import math

from farey.data import Rational
from farey.utils import almost_equal

ALLOWED_METHODS = ["farey"]


def farey_add(x: Rational, y: Rational) -> Rational:
    """ Find the mediant of two rational numbers, as a rational number. """
    return Rational(x.numerator + y.numerator, x.denominator + y.denominator)


def find_rational_approximation(x, method="farey", places=None, max_denominator=None):
    """Find a rational approximation of x to the specified number of decimal places.

    We use an algorithm based on the Farey sequence, which consists of all completely
    reduced fractions between 0 and 1. This ensures that the rational approximation
    found by the algorithm is completely reduced.
    """
    if x == 0:
        return Rational(0, 1)
    elif x < 0:
        return -find_rational_approximation(-x, method, places, max_denominator)
    elif x >= 1:
        return int(x // 1) + find_rational_approximation(
            x % 1, method, places, max_denominator
        )
    elif 0.5 < x < 1:
        return 1 - find_rational_approximation(1 - x, method, places, max_denominator)

    if method == "farey":
        if places is not None and max_denominator is None:
            return _farey_algorithm_accuracy(x, places)
        if places is None and max_denominator is not None:
            return _farey_algorithm_denominator(x, max_denominator)
        else:
            raise ValueError("must specify one of places or max_denominator")
    else:
        raise ValueError("method should be one of %s" % ALLOWED_METHODS)


def _farey_algorithm_accuracy(x, places=7):
    """Find a rational approximation of x to the specified number of decimal places.

    We use an algorithm based on the Farey sequence, which consists of all completely
    reduced fractions between 0 and 1. This ensures that the rational approximation
    found by the algorithm is completely reduced.

    To speed up the process for small x, note that we only need to look in the range between
    (0, 1) and (1, N), for N = math.floor(1 / x), since we will always reach this region
    eventually by repeated Farey addition.
    """

    left = Rational(0, 1)
    right = Rational(1, math.floor(1 / x))
    if almost_equal(x, left, places):
        return left
    elif almost_equal(x, right, places):
        return right

    mediant = None

    while mediant is None or not almost_equal(x, mediant, places):
        mediant = farey_add(left, right)
        if x < mediant:
            right = mediant
        elif x > mediant:
            left = mediant
        else:
            return mediant

    return mediant


def _farey_algorithm_denominator(x, max_denominator=1000):
    """Find a rational approximation of x with denominator no larger than that specified.

    We use an algorithm based on the Farey sequence, which consists of all completely
    reduced fractions between 0 and 1. This ensures that the rational approximation
    found by the algorithm is completely reduced.

    To speed up the process for small x, note that we only need to look in the range between
    (0, 1) and (1, N), for N = math.floor(1 / x), since we will always reach this region
    eventually by repeated Farey addition.
    """

    N = math.floor(1 / x)
    if max_denominator <= N:
        return min(
            [Rational(0, 1), Rational(1, max_denominator)], key=lambda r: abs(x - r)
        )

    left = Rational(0, 1)
    right = Rational(1, N)

    while max(left.denominator, right.denominator) < max_denominator:
        mediant = farey_add(left, right)
        if mediant.denominator > max_denominator:
            # the current bounds are as good as we can do, so have to choose the best of them
            break
        if x < mediant:
            right = mediant
        elif x > mediant:
            left = mediant
        else:
            return mediant

    return min([left, right], key=lambda r: abs(x - r))
