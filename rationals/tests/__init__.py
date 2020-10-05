from rationals.utils import almost_equal


def assert_almost_equal(a, b, places=7, message=None):
    """
    Fail if numbers `a` and `b` are not close enough
    """
    if message is None:
        message = f"{a} !~= {b} to {places} places"
    assert almost_equal(a, b, places), message
