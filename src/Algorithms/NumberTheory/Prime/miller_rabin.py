def _miller_rabin_test(n: int, s: int, d: int, a: int) -> bool:
    """ミラーラビンテストの1回分の計算

    Args:
        n (int): 元の数
        s (int): n - 1 = 2^s * d の最大のs
        d (int): n - 1 = 2^s * d の奇数d
        a (int): テストケース 1 <= a <= n - 1

    Returns:
        bool: True -> 素数, False -> 合成数
    """
    # フェルマーテスト
    if pow(a, n - 1, n) != 1:
        return False

    # ミラーラビンテスト
    # a^d = 1 or a^d = -1
    x = pow(a, d, n)
    if (x == 1) or (x == n - 1):
        return True

    # a^(2^1 * d) = -1 or ... a^(2^(s - 1) * d) = -1
    for _ in range(s):
        x = pow(x, 2, n)
        if x == n - 1:
            return True

    return False


def miller_rabin(n: int) -> bool:
    """nが素数かどうかを確率的に判定する

    Args:
        n (int): 素数かどうかを判定したい数

    Returns:
        bool: True -> 素数, False -> 合成数

    Note:
        n <= 2^64でdeterministic (参考: http://miller-rabin.appspot.com/)
    """
    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # n - 1 = 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    test_case = [2, 7, 61] if n < 4759123141 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in test_case:
        if not (a < n):
            break

        if _miller_rabin_test(n, s, d, a) is False:
            return False
    return True
