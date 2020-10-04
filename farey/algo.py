import math

from farey.data import truncated_continued_fraction, Rational, SimpleContinuedFraction
from farey.utils import almost_equal

ALLOWED_METHODS = ["farey", "continued_fraction"]


def farey_add(x: Rational, y: Rational) -> Rational:
    """ Find the mediant of two rational numbers, as a rational number. """
    return Rational(x.numerator + y.numerator, x.denominator + y.denominator)


def best_rational_approximation(x, method="farey", places=None, max_denominator=None):
    """Find a rational approximation of x to the specified number of decimal places.

    We use an algorithm based on the Farey sequence, which consists of all completely
    reduced fractions between 0 and 1. This ensures that the rational approximation
    found by the algorithm is completely reduced.
    """
    if x == 0:
        return Rational(0, 1)
    elif x < 0:
        return -best_rational_approximation(-x, method, places, max_denominator)
    elif x >= 1:
        return int(x // 1) + best_rational_approximation(
            x % 1, method, places, max_denominator
        )
    elif 0.5 < x < 1:
        return 1 - best_rational_approximation(1 - x, method, places, max_denominator)

    if method == "farey":
        if places is not None and max_denominator is None:
            return _farey_algorithm_accuracy(x, places)
        if places is None and max_denominator is not None:
            return _farey_algorithm_denominator(x, max_denominator)
        else:
            raise ValueError("must specify one of places or max_denominator")
    elif method == "continued_fraction":
        if places is not None and max_denominator is None:
            return _continued_fraction_algorithm_accuracy(x, places)
        elif places is None and max_denominator is not None:
            return _continued_fraction_algorithm_denominator(x, max_denominator)
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


def _continued_fraction_algorithm_denominator(x, max_denominator=1000):
    """Find a rational approximation of x with denominator no larger than that specified.

    We use an algorithm based on truncating the continued fraction representation of a number,
    and reducing its final value until reaching a suitable rational representation,
    cf. https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations.
    """
    n = 0
    prev_denominator = 0  # k_{-1} = 0
    current_convergent = Rational(math.floor(x), 1)

    while True:
        next_truncation = truncated_continued_fraction(x, n + 1)
        next_convergent = next_truncation.as_rational
        if next_convergent == current_convergent:
            # reached the end of finite continued fraction
            return current_convergent
        if next_convergent.denominator > max_denominator:
            # we've gone too far so need to find potential convergents by reducing the last value
            # of the continued fraction, without going past half of a_{n+1}.
            # The smallest we can make the denominator in this way is given by
            # math.ceil(a_{n+1} / 2) * k_n + k_{n-1}
            a_n_plus_one = next_truncation.last_value
            smallest_denominator = (
                math.ceil(a_n_plus_one / 2) * current_convergent.denominator
                + prev_denominator
            )
            if smallest_denominator > max_denominator:
                # we can't get better than the approximation we already have
                return current_convergent
            else:
                # there is some i for which the reduced denominator is less than max_denominator
                # k'_{n+1} = (a_{n+1} - i) * k_n + k_{n-1} < max_denominator
                # The smallest such i is math.ceil((k_{n+1} - max_denominator) / k_n)
                optimal_reduction_factor = math.ceil(
                    (next_convergent.denominator - max_denominator)
                    / current_convergent.denominator
                )
                next_truncation = next_truncation.replace_last_value(
                    a_n_plus_one - optimal_reduction_factor
                )
                next_convergent = next_truncation.as_rational
                # if a_{n+1} is even and i == a_{n+1} / 2, we need to check the errors
                if (
                    a_n_plus_one % 2 == 0
                    and optimal_reduction_factor == a_n_plus_one / 2
                ):
                    current_error = abs(x - current_convergent)
                    next_error = abs(x - next_convergent)
                    if next_error < current_error:
                        return next_convergent
                    else:
                        return current_convergent
                else:
                    return next_convergent
        else:
            n += 1
            prev_denominator = current_convergent.denominator
            current_convergent = next_convergent


def _continued_fraction_algorithm_accuracy(x, places=7):
    epsilon = 0.5 * 10 ** -places
    n = 0
    current_convergent = Rational(math.floor(x), 1)
    if almost_equal(x, current_convergent, places=places):
        return current_convergent

    while True:
        next_truncation = truncated_continued_fraction(x, n + 1)
        next_convergent = next_truncation.as_rational
        if almost_equal(x, next_convergent, places=places):
            # we're within the allowed bound, but may be able to find a convergent
            # with smaller denominator also within the bound by reducing the last
            # value of the continued fraction.
            bound = x + (1 if n % 2 == 0 else -1) * epsilon
            optimal_reduction_factor = math.floor(
                (next_convergent.numerator - next_convergent.denominator * bound)
                / (
                    current_convergent.numerator
                    - current_convergent.denominator * bound
                )
            )
            a_n_plus_one = next_truncation.last_value
            next_truncation = next_truncation.replace_last_value(
                a_n_plus_one - optimal_reduction_factor
            )
            return next_truncation.as_rational
        else:
            n += 1
            current_convergent = next_convergent
