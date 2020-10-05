def almost_equal(a, b, places=7):
    return a == b or abs(a - b) < 0.5 * 10 ** -places
