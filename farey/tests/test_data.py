from farey.data import Rational


def test_rational_addition():
    x = Rational(1, 2)  # 1/2
    y = Rational(3, 5)  # 3/5
    assert x + y == Rational(11, 10)


def test_integer_addition():
    x = Rational(1, 2)
    assert x + 1 == 1 + x == Rational(3, 2)


def test_rational_multiplication():
    x = Rational(1, 2)
    y = Rational(3, 5)
    assert x * y == Rational(3, 10)


def test_integer_multiplication():
    x = Rational(1, 2)
    z = 4
    assert x * z == z * x == Rational(4, 2)


def test_float_multiplication():
    x = Rational(1, 2)
    z = 3.2
    assert x * z == z * x == 1.6


def test_negative():
    x = Rational(1, 2)
    assert -x == Rational(-1, 2)


def test_float():
    x = Rational(1, 2)
    assert float(x) == 0.5
