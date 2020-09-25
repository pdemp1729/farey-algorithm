import math

from farey.data import Rational
from farey.utils import almost_equal


def farey_add(x: Rational, y: Rational) -> Rational:
    """ Find the mediant of two rational numbers, as a rational number. """
    return Rational(x.numerator + y.numerator, x.denominator + y.denominator)


def find_rational_approximation(x, places=7):
    """Find a rational approximation of x to the specified number of decimal places.

    We use an algorithm based on the Farey sequence, which consists of all completely
    reduced fractions between 0 and 1. This ensures that the rational approximation
    found by the algorithm is completely reduced.
    """
    if x == 0:
        return Rational(0, 1)
    elif x < 0:
        return -find_rational_approximation(-x, places)
    elif x >= 1:
        return int(x // 1) + find_rational_approximation(x % 1, places)
    elif 0.5 < x < 1:
        return 1 - find_rational_approximation(1 - x, places)

    # we only need to look in the range between (0, 1)
    # and (1, n) for n = math.floor(1 / x), since we will always reach
    # this eventually by the Farey addition

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
