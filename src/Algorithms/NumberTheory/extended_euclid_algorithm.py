def extended_euclid(a: int, b: int):
    """拡張ユークリッドの互除法
    ax + by = gcd(a, b)の整数解を求める.

    Args:
        a (int): ax + byのa
        b (int): ax + byのb

    Returns:
        g (int): gcd(a, b)
        x (int): a*x + b*y = d を満たすx
        y (int): a*x + b*y = d を満たすy
    """
    if b == 0:
        return a, 1, 0

    q = a // b
    r = a % b

    g, s, t = extended_euclid(b, r)
    x, y = t, s - q * t
    return g, x, y


if __name__ == "__main__":
    a, b = map(int, input().split())
    _, x, y = extended_euclid(a, b)
    print(x, y)
