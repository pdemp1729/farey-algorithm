import math

from pytest import raises

from farey.data import Rational


def test_rational_zero():
    x = Rational(0, 1)
    assert x.is_zero
    with raises(ZeroDivisionError):
        _ = x.inverse


def test_rational_addition():
    x = Rational(1, 2)  # 1/2
    y = Rational(3, 5)  # 3/5

    # Rational + Rational -> Rational
    assert x + y == Rational(11, 10)
    # Rational + int -> Rational
    assert x + 1 == 1 + x == Rational(3, 2)
    # Rational + float -> float
    assert x + 0.1 == 0.1 + x == 0.6

    with raises(TypeError) as excinfo:
        _ = x + "a"
    assert str(excinfo.value) == "must be int, float or Rational, not str"


def test_rational_subtraction():
    x = Rational(1, 2)  # 1/2
    y = Rational(3, 5)  # 3/5
    assert x - y == Rational(-1, 10)


def test_rational_multiplication():
    x = Rational(1, 2)
    y = Rational(3, 5)

    # Rational * Rational -> Rational
    assert x * y == Rational(3, 10)
    # Rational * int -> Rational
    assert x * 4 == 4 * x == Rational(4, 2)
    # Rational * float -> float
    assert x * 3.2 == 3.2 * x == 1.6

    with raises(TypeError) as excinfo:
        _ = x * "a"
    assert str(excinfo.value) == "must be int, float or Rational, not str"


def test_rational_division():
    x = Rational(1, 2)
    y = Rational(3, 5)
    z = Rational(-4, 7)

    # Rational / (non-zero) Rational -> Rational
    assert x / y == Rational(5, 6)
    assert x / z == Rational(-7, 8)
    with raises(ZeroDivisionError):
        _ = x / Rational(0, 1)

    # Rational / (non-zero) int -> Rational
    assert x / 2 == Rational(1, 4)
    assert x / -2 == Rational(-1, 4)
    with raises(ZeroDivisionError):
        _ = x / 0

    # Rational / float -> float
    assert y / 1.2 == 0.5


def test_rational_power():
    x = Rational(2, 3)
    # Rational ** int -> Rational
    assert x ** 3 == Rational(8, 27)
    assert x ** -3 == Rational(27, 8)
    assert x ** 0 == Rational(1, 1)
    # Rational ** float -> float
    assert x ** 0.5 == 0.816496580927726
    # edge cases
    with raises(ZeroDivisionError):
        _ = Rational(0, 1) ** -1
    assert Rational(0, 1) ** 0 == Rational(1, 1)


def test_rational_comparison():
    x = Rational(1, 2)
    y = Rational(2, 3)

    assert x < y and y > x
    assert 0 < x < 1

    with raises(TypeError) as excinfo:
        _ = x < "1"
    assert str(excinfo.value) == "must be int, float or Rational, not str"

    with raises(TypeError) as excinfo:
        _ = x > "0"
    assert str(excinfo.value) == "must be int, float or Rational, not str"


def test_rational_negative():
    x = Rational(1, 2)
    neg_x = -x
    assert neg_x == Rational(-1, 2)
    assert neg_x.is_negative


def test_rational_float():
    x = Rational(1, 2)
    assert float(x) == 0.5


def test_rational_floor():
    x = Rational(5, 2)
    y = Rational(-1, 2)
    z = Rational(1, 1)
    assert math.floor(x) == 2
    assert math.floor(y) == -1
    assert math.floor(z) == 1


def test_rational_ceil():
    x = Rational(5, 2)
    y = Rational(-1, 2)
    z = Rational(1, 1)
    assert math.ceil(x) == 3
    assert math.ceil(y) == 0
    assert math.ceil(z) == 1


def test_rational_inverse():
    x = Rational(1, 3)
    assert x.inverse == Rational(3, 1)

    x = Rational(-2, 5)
    assert x.inverse == Rational(-5, 2)


def test_rational_repr():
    x = Rational(1, 2)
    assert repr(x) == "1/2"


def test_rational_reduction():
    x = Rational(1, 3)
    y = Rational(2, 6)
    z = Rational(0, 3)

    assert x != y

    assert x.is_reduced
    assert not y.is_reduced
    assert not z.is_reduced
    assert y.reduced_form == x
    assert z.reduced_form == Rational(0, 1)
