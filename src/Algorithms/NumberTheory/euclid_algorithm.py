def euclid_algorithm(a: int, b: int):
    """aとbの最大公約数を求める.

    Args:
        a (int): 整数
        b (int): 整数

    Returns:
        int: gcd(a, b)
    """
    if b == 0:
        return a
    return euclid_algorithm(b, a % b)


def gcd(a: int, b: int):
    """aとbの最大公約数

    Args:
        a (int): 整数
        b (int): 整数

    Retuns:
        int: gcd(a, b)
    """
    return euclid_algorithm(a, b)
