# farey-algorithm
An implementation of various algorithms for approximating real numbers by rationals.

## Usage

To import the module, simply do
```
import rationals
```

To find the nearest rational approximation accurate to a certain number of decimal places,
use the `places` kwarg:
```
rationals.best_rational_approximation(
    math.sqrt(2), method="farey", places=5,
)
```

To find the nearest rational approximation with denominator no larger than some cutoff, use
the `max_denominator` kwarg:
```
rationals.best_rational_approximation(
    math.sqrt(2), method="farey", max_denominator=1000,
)
```

The available methods are `"farey"` and `"continued_fraction"`.
