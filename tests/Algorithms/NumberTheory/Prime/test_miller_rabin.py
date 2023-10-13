from src.Algorithms.NumberTheory.Prime.miller_rabin import miller_rabin


def test_miller_rabin():
    assert miller_rabin(7) is True
    assert miller_rabin(6) is False
    assert miller_rabin(1) is False
    assert miller_rabin(2) is True
    assert miller_rabin(3) is True
    assert miller_rabin(4) is False
    assert miller_rabin(998244353) is True
    assert miller_rabin(10 ** 9 + 7) is True
    assert miller_rabin(1000000000000000000) is False


def test_miller_rabin_prime():

    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271
    ]
    for p in primes:
        assert miller_rabin(p) is True
