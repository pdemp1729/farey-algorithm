import math


class Rational:
    """Data structure representing a rational number.

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
        """Addition has the following properties:
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
                self.denominator * other.denominator,
            )
        elif isinstance(other, int):
            return Rational(self.numerator + other * self.denominator, self.denominator)
        elif isinstance(other, float):
            return other + float(self)
        else:
            raise TypeError(
                "must be int, float or Rational, not %s" % type(other).__name__
            )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __mul__(self, other):
        """Multiplication has the following properties:
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
                self.numerator * other.numerator, self.denominator * other.denominator
            )
        elif isinstance(other, int):
            return Rational(self.numerator * other, self.denominator)
        elif isinstance(other, float):
            return float(self) * other
        else:
            raise TypeError(
                "must be int, float or Rational, not %s" % type(other).__name__
            )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """Division has the following properties:
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
                return Rational(
                    self.numerator * other.denominator,
                    self.denominator * other.numerator,
                )
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
            if power > 0:
                return Rational(self.numerator ** power, self.denominator ** power)
            elif power < 0:
                if self.is_zero:
                    raise ZeroDivisionError
                else:
                    return Rational(
                        self.denominator ** abs(power), self.numerator ** abs(power)
                    )
            else:
                # convention that 0 ** 0 = 1 in python
                return Rational(1, 1)
        else:
            return pow(float(self), power, modulo)

    def __eq__(self, other):
        """Two rational numbers are considered equal if they have the same numerator and denominator.

        >>> Rational(1, 2) == Rational(1, 2)
        True
        >>> Rational(1, 2) == Rational(2, 4)
        False
        """
        if not isinstance(other, Rational):
            return False
        return (
            self.denominator == other.denominator and self.numerator == other.numerator
        )

    def __lt__(self, other):
        """Ordering of rational numbers is implemented using their float representations.

        >>> Rational(1, 2) < Rational(3, 4)
        True
        """
        if isinstance(other, (Rational, int, float)):
            return float(self) < float(other)
        else:
            raise TypeError(
                "must be int, float or Rational, not %s" % type(other).__name__
            )

    def __gt__(self, other):
        """Ordering of rational numbers is implemented using their float representations.

        >>> Rational(1, 2) > Rational(3, 4)
        False
        """
        if isinstance(other, (Rational, int, float)):
            return float(self) > float(other)
        else:
            raise TypeError(
                "must be int, float or Rational, not %s" % type(other).__name__
            )

    def __neg__(self):
        """The negative of a Rational number

        >>> -Rational(1, 2)
        -1/2
        """
        return Rational(-self.numerator, self.denominator)

    def __float__(self):
        """The float representation is obtained by evaluating the fraction.

        >>> float(Rational(1, 2))
        0.5
        """
        return self.numerator / self.denominator

    def __abs__(self):
        """Only the numerator is an unsigned int, so we take the absolute value of that.

        >>> abs(Rational(-1, 2))
        1/2
        """
        return Rational(abs(self.numerator), self.denominator)

    def __floor__(self):
        """For use with math.floor function."""
        return self.numerator // self.denominator

    def __ceil__(self):
        """For use with math.ceil function."""
        return self.numerator // self.denominator + (
            self.numerator % self.denominator > 0
        )

    def __repr__(self):
        return "{}/{}".format(self.numerator, self.denominator)


def simplify(x: Rational) -> Rational:
    """ Reduce rational number to its simplest terms """
    if x.is_zero:
        return Rational(0, 1)
    else:
        gcd = math.gcd(x.numerator, x.denominator)
        return Rational(x.numerator // gcd, x.denominator // gcd)


class SimpleContinuedFraction:
    """Data structure representing a finite simple continued fraction.

    A finite simple continued fraction is an expression of the form
    a_0 + 1 / (a_1 + 1 / (... + 1 / a_n)),
    where the a_i are integers, and all a_i except for a_0 are positive,
    cf. https://en.wikipedia.org/wiki/Continued_fraction.

    >>> SimpleContinuedFraction(1, 2, 3)
    [1; 2, 3]
    """

    def __init__(self, *args):
        assert len(args) > 0, "must provide at least one argument"
        self._list_representation = list(args)

    @property
    def has_leading_zero(self):
        return self[0] == 0

    @property
    def is_zero(self):
        return len(self) == 1 and self.has_leading_zero

    @property
    def inverse(self):
        if self.is_zero:
            raise ZeroDivisionError
        elif self.has_leading_zero:
            return self[1:]
        else:
            return SimpleContinuedFraction(0, *self)

    @property
    def as_rational(self) -> Rational:
        if len(self) == 1:
            return Rational(self[0], 1)
        elif len(self) == 2:
            return self[0] + Rational(1, self[1])
        else:
            return self[0] + self[1:].as_rational.inverse

    @classmethod
    def from_rational(cls, r: Rational) -> "SimpleContinuedFraction":
        list_repr = []
        while True:
            int_part = math.floor(r)
            list_repr.append(int_part)
            try:
                r = (r - int_part).inverse
            except ZeroDivisionError:
                break
        return cls(*list_repr)

    def __eq__(self, other):
        if not isinstance(other, SimpleContinuedFraction):
            return False
        return self._list_representation == other._list_representation

    def __iter__(self):
        return self._list_representation.__iter__()

    def __getitem__(self, item):
        """Slicing returns another SimpleContinuedFraction, whereas integer indexing returns an int.

        >>> SimpleContinuedFraction(1, 2, 3)[0]
        1
        >>> SimpleContinuedFraction(1, 2, 3)[1:]
        [2; 3]
        """
        list_repr = self._list_representation.__getitem__(item)
        if isinstance(item, slice):
            return SimpleContinuedFraction(*list_repr)
        else:
            return list_repr

    def __len__(self):
        return len(self._list_representation)

    def __float__(self):
        """The float representation is obtained by evaluating the continued fraction."""
        if len(self) == 1:
            return float(self[0])
        elif len(self) == 2:
            return self[0] + 1 / float(self[1])
        else:
            return self[0] + 1 / float(self[1:])

    def __repr__(self):
        first = self._list_representation[0]
        others = [str(x) for x in self._list_representation[1:]]
        return f"[{first}; {', '.join(others)}]"


def truncated_continued_fraction(x: float, n: int) -> SimpleContinuedFraction:
    """Truncate the continued fraction representation of x at the (n+1)'th term."""
    list_repr = []
    while len(list_repr) <= n:
        int_part = math.floor(x)
        list_repr.append(int_part)
        try:
            x = 1 / (x - int_part)
        except ZeroDivisionError:
            break
    return SimpleContinuedFraction(*list_repr)


def convergent(x: float, n: int) -> Rational:
    """Calculate the n'th convergent of the number x.

    The n'th convergent of x is obtained by truncating the continued fraction expansion
    of x at the (n+1)'th term and calculating its rational representation. This is guaranteed
    to be in lowest terms.

    The even convergents are underestimates of x, while the odd convergents are overestimates,
    which get closer to x as n is increased.
    """
    continued_frac = truncated_continued_fraction(x, n)
    return continued_frac.as_rational
