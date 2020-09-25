import math


class Rational:
    """ Data structure representing a rational number.

    We store a rational number as a tuple of integers (one unsigned, one positive)
    representing the numerator and denominator of the corresponding fraction.

    >>> Rational(1, 2)
    1/2
    """
    def __init__(self, numerator, denominator):
        assert denominator > 0
        self.numerator = numerator
        self.denominator = denominator

    @property
    def is_zero(self):
        return self.numerator == 0

    @property
    def is_negative(self):
        return self.numerator < 0

    @property
    def inverse(self):
        if self.is_zero:
            raise ZeroDivisionError
        elif self.is_negative:
            return Rational(-self.denominator, abs(self.numerator))
        else:
            return Rational(self.denominator, self.numerator)

    @property
    def is_reduced(self):
        gcd = math.gcd(self.numerator, self.denominator)
        return gcd == 1

    @property
    def reduced_form(self):
        return simplify(self)

    def __add__(self, other):
        """ Addition has the following properties:
        - Rational + Rational -> Rational
        - Rational + int -> Rational
        - Rational + float -> float

        >>> Rational(1, 2) + Rational(1, 4)
        6/8
        >>> Rational(1, 2) + 3
        7/2
        >>> Rational(1, 2) + 0.25
        0.75
        """
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.denominator + self.denominator * other.numerator,
                self.denominator * other.denominator
            )
        elif isinstance(other, int):
            return Rational(self.numerator + other * self.denominator, self.denominator)
        elif isinstance(other, float):
            return other + float(self)
        else:
            return

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __mul__(self, other):
        """ Multiplication has the following properties:
        - Rational * Rational -> Rational
        - Rational * int -> Rational
        - Rational * float -> float

        >>> Rational(1, 2) * Rational(1, 3)
        1/6
        >>> Rational(1, 2) * 3
        3/2
        >>> Rational(1, 2) * 3.4
        1.7
        """
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.numerator,
                self.denominator * other.denominator
            )
        elif isinstance(other, int):
            return Rational(self.numerator * other, self.denominator)
        elif isinstance(other, float):
            return float(self) * other
        else:
            return

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """ Division has the following properties:
        - Rational / (non-zero) Rational -> Rational
        - Rational / (non-zero) int -> Rational
        - Rational / (non-zero) float -> float
        - Rational / zero -> ZeroDivisionError

        >>> Rational(1, 2) / Rational(3, 4)
        4/6
        >>> Rational(1, 2) / 3
        1/6
        """
        if isinstance(other, Rational):
            if other.is_zero:
                raise ZeroDivisionError
            elif other.is_negative:
                return -self / abs(other)
            else:
                return Rational(self.numerator * other.denominator, self.denominator * other.numerator)
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError
            elif other < 0:
                return -self / abs(other)
            else:
                return Rational(self.numerator, self.denominator * other)
        else:
            return float(self) / other

    def __pow__(self, power, modulo=None):
        """
        For integer powers, raise the numerator and denominator to the same power,
        else revert to __pow__() applied to the float representation.

        >>> Rational(2, 3) ** 3
        8/27
        """
        if isinstance(power, int) and modulo is None:
            return Rational(self.numerator ** power, self.denominator ** power)
        else:
            return pow(float(self), power, modulo)

    def __eq__(self, other):
        """ Two rational numbers are considered equal if they have the same numerator and denominator.

        >>> Rational(1, 2) == Rational(1, 2)
        True
        >>> Rational(1, 2) == Rational(2, 4)
        False
        """
        if not isinstance(other, Rational):
            return False
        return self.denominator == other.denominator and self.numerator == other.numerator

    def __lt__(self, other):
        """ Ordering of rational numbers is implemented using their float representations.

        >>> Rational(1, 2) < Rational(3, 4)
        True
        """
        if isinstance(other, (Rational, int, float)):
            return float(self) < float(other)
        else:
            return

    def __gt__(self, other):
        """ Ordering of rational numbers is implemented using their float representations.

        >>> Rational(1, 2) > Rational(3, 4)
        False
        """
        if isinstance(other, (Rational, int, float)):
            return float(self) > float(other)
        else:
            return

    def __neg__(self):
        """ The negative of a Rational number

        >>> -Rational(1, 2)
        -1/2
        """
        return Rational(-self.numerator, self.denominator)

    def __float__(self):
        """ The float representation is obtained by evaluating the fraction.

        >>> float(Rational(1, 2))
        0.5
        """
        return self.numerator / self.denominator

    def __abs__(self):
        """ Only the numerator is an unsigned int, so we take the absolute value of that.

        >>> abs(Rational(-1, 2))
        1/2
        """
        return Rational(abs(self.numerator), self.denominator)

    def __repr__(self):
        return "{}/{}".format(self.numerator, self.denominator)


def simplify(x: Rational) -> Rational:
    """ Reduce rational number to its simplest terms """
    if x.is_zero:
        return Rational(0, 1)
    else:
        gcd = math.gcd(x.numerator, x.denominator)
        return Rational(x.numerator // gcd, x.denominator // gcd)
