def pow(a: int, x: int, mod: int = 1) -> int:
    """a^x % modを計算する (modは任意)

    Args:
        a (int): base
        x (int): power
        mod (int): mod

    Returns:
        int: a^x % mod
    """
    result = 1
    base = a

    while x:
        # 最下位のbitが1 <=> 奇数
        if x % 2:
            result *= base
            result %= mod

        base *= base
        base %= mod

        # 右ビットシフト
        x >>= 1
    return result


if __name__ == "__main__":
    mod = 1000000007
    m, n = map(int, input().split())
    print(pow(m, n, mod))
