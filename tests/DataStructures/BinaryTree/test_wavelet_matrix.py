from itertools import combinations
from collections import Counter

from src.DataStructures.BinaryTree.wavelet_matrix import WaveletMatrix


def test_access():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    assert wm.access(0) == 5
    assert wm.access(1) == 4
    assert wm.access(2) == 5
    assert wm.access(3) == 5
    assert wm.access(4) == 2
    assert wm.access(5) == 1
    assert wm.access(6) == 5
    assert wm.access(7) == 6
    assert wm.access(8) == 1
    assert wm.access(9) == 3
    assert wm.access(10) == 5
    assert wm.access(11) == 0


def test_get_item():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    assert wm[0] == 5
    assert wm[1] == 4
    assert wm[2] == 5
    assert wm[3] == 5
    assert wm[4] == 2
    assert wm[5] == 1
    assert wm[6] == 5
    assert wm[7] == 6
    assert wm[8] == 1
    assert wm[9] == 3
    assert wm[10] == 5
    assert wm[11] == 0


def test_get_i_bit():
    wm = WaveletMatrix([4, 4, 5, 5])

    # 5 = 101
    assert wm._get_i_bit(5, 0) == 1
    assert wm._get_i_bit(5, 1) == 0
    assert wm._get_i_bit(5, 2) == 1
    assert wm._get_i_bit(5, 3) == 0

    # 4 = 100
    assert wm._get_i_bit(4, 0) == 0
    assert wm._get_i_bit(4, 1) == 0
    assert wm._get_i_bit(4, 2) == 1
    assert wm._get_i_bit(4, 3) == 0


def test_rank():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[0..7) = [5, 4, 5, 5, 2, 1, 5]
    assert wm.rank(0, 7) == 0
    assert wm.rank(1, 7) == 1
    assert wm.rank(2, 7) == 1
    assert wm.rank(4, 7) == 1
    assert wm.rank(5, 7) == 4

    for x in range(8):
        for right in range(1, len(T) + 1):
            expected = T[:right].count(x)
            actual = wm.rank(x, right)
            assert actual == expected


def test_rank_range():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.rank_range(0, 1, 10) == 0
    assert wm.rank_range(1, 1, 10) == 2
    assert wm.rank_range(2, 1, 10) == 1
    assert wm.rank_range(3, 1, 10) == 1
    assert wm.rank_range(4, 1, 10) == 1
    assert wm.rank_range(5, 1, 10) == 3
    assert wm.rank_range(6, 1, 10) == 1

    # 変な範囲を指定したケース
    assert wm.rank_range(6, 1, 1) == 0
    assert wm.rank_range(6, 4, 3) == 0
    assert wm.rank_range(100, 0, 10) == 0
    assert wm.rank_range(-10, 0, 10) == 0

    for left, right in combinations(range(len(T)), r=2):
        for x in range(7):
            expected = T[left:right].count(x)
            actual = wm.rank_range(x, left, right)
            assert actual == expected


def test_select():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    assert wm.select(0, 1) == 11

    assert wm.select(1, 1) == 5
    assert wm.select(1, 2) == 8

    assert wm.select(2, 1) == 4

    assert wm.select(3, 1) == 9

    assert wm.select(4, 1) == 1

    assert wm.select(5, 1) == 0
    assert wm.select(5, 2) == 2
    assert wm.select(5, 3) == 3
    assert wm.select(5, 4) == 6
    assert wm.select(5, 5) == 10

    assert wm.select(6, 1) == 7

    # 変な値を指定したケース
    T = [5, 4, 5, 5, 2, 0, 5, 6, 2, 3, 7, 7]
    wm = WaveletMatrix(T)
    assert wm.select(-1, 1) is None
    assert wm.select(7, 1) == 10
    assert wm.select(8, 1) is None
    assert wm.select(7, 0) is None
    assert wm.select(7, -1) is None
    assert wm.select(0, 1) == 5
    assert wm.select(1, 1) is None
    assert wm.select(1, 0) is None

    T = [3, 3, 3, 3, 3]
    wm = WaveletMatrix(T)
    assert wm.select(0, 1) is None
    assert wm.select(1, 1) is None
    assert wm.select(2, 2) is None

    T = [3, 3, 4, 4, 4]
    wm = WaveletMatrix(T)
    assert wm.select(3, 3) is None
    assert wm.select(4, 4) is None


def test_quantile():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # sorted(T[1..10)) = [1, 1, 2, 3, 4, 5, 5, 5, 6,]
    assert wm.quantile(1, 10, 1) == 1
    assert wm.quantile(1, 10, 2) == 1
    assert wm.quantile(1, 10, 3) == 2
    assert wm.quantile(1, 10, 4) == 3
    assert wm.quantile(1, 10, 5) == 4
    assert wm.quantile(1, 10, 6) == 5
    assert wm.quantile(1, 10, 7) == 5
    assert wm.quantile(1, 10, 8) == 5
    assert wm.quantile(1, 10, 9) == 6

    for left, right in combinations(range(len(T)), r=2):
        for k in range(1, right - left + 1):
            expected = sorted(T[left:right])[k - 1]
            actual = wm.quantile(left, right, k)
            assert actual == expected

    # 変な範囲を指定したケース
    T = [3, 3, 3, 4, 4]
    wm = WaveletMatrix(T)
    assert wm.quantile(0, 5, 0) is None
    assert wm.quantile(0, 5, 1) == 3
    assert wm.quantile(0, 5, 2) == 3
    assert wm.quantile(0, 5, 3) == 3
    assert wm.quantile(0, 5, 4) == 4
    assert wm.quantile(0, 5, 5) == 4
    assert wm.quantile(0, 5, 6) is None
    assert wm.quantile(0, 5, 7) is None


def test_kth_smallest():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # sorted(T[1..10)) = [1, 1, 2, 3, 4, 5, 5, 5, 6,]
    assert wm.kth_smallest(1, 10, 1) == 1
    assert wm.kth_smallest(1, 10, 2) == 1
    assert wm.kth_smallest(1, 10, 3) == 2
    assert wm.kth_smallest(1, 10, 4) == 3
    assert wm.kth_smallest(1, 10, 5) == 4
    assert wm.kth_smallest(1, 10, 6) == 5
    assert wm.kth_smallest(1, 10, 7) == 5
    assert wm.kth_smallest(1, 10, 8) == 5
    assert wm.kth_smallest(1, 10, 9) == 6

    for left, right in combinations(range(len(T)), r=2):
        for k in range(1, right - left + 1):
            expected = sorted(T[left:right])[k - 1]
            actual = wm.kth_smallest(left, right, k)
            assert actual == expected


def test_kth_largest():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # sorted(T[1..10)) = [1, 1, 2, 3, 4, 5, 5, 5, 6,]
    assert wm.kth_largest(1, 10, 1) == 6
    assert wm.kth_largest(1, 10, 2) == 5
    assert wm.kth_largest(1, 10, 3) == 5
    assert wm.kth_largest(1, 10, 4) == 5
    assert wm.kth_largest(1, 10, 5) == 4
    assert wm.kth_largest(1, 10, 6) == 3
    assert wm.kth_largest(1, 10, 7) == 2
    assert wm.kth_largest(1, 10, 8) == 1
    assert wm.kth_largest(1, 10, 9) == 1

    for left, right in combinations(range(len(T)), r=2):
        for k in range(1, right - left + 1):
            expected = sorted(T[left:right])[::-1][k - 1]
            actual = wm.kth_largest(left, right, k)
            assert actual == expected


def test_topk():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.topk(1, 10, 2) == [(5, 3), (1, 2)]
    assert wm.topk(1, 10, 3) == [(5, 3), (1, 2), (2, 1)]
    assert wm.topk(1, 10, 4) == [(5, 3), (1, 2), (2, 1), (3, 1)]
    assert wm.topk(1, 10, 5) == [(5, 3), (1, 2), (2, 1), (3, 1), (4, 1)]

    # 変な範囲を指定したケース
    assert wm.topk(4, 3, 10) == []
    assert wm.topk(4, 4, 10) == []
    assert wm.topk(1, 10, 0) == []
    assert wm.topk(1, 10, -1) == []

    for left, right in combinations(range(len(T)), r=2):
        counter = Counter(T[left:right])
        counter = sorted(
            [(key, value) for key, value in counter.items()],
            key=lambda x: (-x[1], x[0]),
        )
        for k in range(1, right - left + 1):
            expected = counter[:k]
            actual = wm.topk(left, right, k)
            assert actual == expected


def test_sum():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)
    assert wm.sum(1, 10) == 32

    # 変な範囲を指定したケース
    assert wm.sum(1, 1) == 0
    assert wm.sum(4, 3) == 0

    for left, right in combinations(range(len(T)), r=2):
        assert wm.sum(left, right) == sum(T[left:right])


def test_range_freq_to():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.range_freq_to(1, 10, 5) == 5
    assert wm.range_freq_to(4, 8, 4) == 2

    for left, right in combinations(range(len(T)), r=2):
        for upper in range(1, 8):
            expected = len([t for t in T[left:right] if t < upper])
            actual = wm.range_freq_to(left, right, upper)
            assert actual == expected

    # b"111"より大きいケース
    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.range_freq_to(1, 10, 8) == 9
    assert wm.range_freq_to(1, 10, 10000) == 9

    T = [5, 4, 5, 5, 2, 1, 7, 6, 1, 3, 5, 7]
    wm = WaveletMatrix(T)
    assert wm.range_freq_to(1, 10, 8) == 9


def test_range_freq_from():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.range_freq_from(1, 10, 0) == 9
    assert wm.range_freq_from(1, 10, 1) == 9
    assert wm.range_freq_from(1, 10, 2) == 7
    assert wm.range_freq_from(1, 10, 3) == 6
    assert wm.range_freq_from(1, 10, 4) == 5
    assert wm.range_freq_from(1, 10, 5) == 4
    assert wm.range_freq_from(1, 10, 6) == 1
    assert wm.range_freq_from(1, 10, 7) == 0

    for left, right in combinations(range(len(T)), r=2):
        for lower in range(8):
            expected = len([t for t in T[left:right] if lower <= t])
            actual = wm.range_freq_from(left, right, lower)
            assert actual == expected

    # 変な範囲を指定したケース
    T = [5, 4, 5, 5, 2, 7, 5, 6, 1, 3, 5, 7]
    wm = WaveletMatrix(T)
    # T[1..10) = [4, 5, 5, 2, 7, 5, 6, 1, 3]
    assert wm.range_freq_from(1, 10, 7) == 1
    assert wm.range_freq_from(1, 10, 8) == 0
    assert wm.range_freq_from(1, 10, 100) == 0


def test_range_freq():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    assert wm.range_freq(1, 10, 4, 6) == 4
    assert wm.range_freq(4, 8, 5, 7) == 2

    for left, right in combinations(range(len(T)), r=2):
        for lower, upper in combinations(range(8), r=2):
            expected = len([t for t in T[left:right] if lower <= t < upper])
            actual = wm.range_freq(left, right, lower, upper)
            assert actual == expected

    # 変な範囲を指定したケース
    T = [5, 4, 5, 5, 2, 7, 5, 6, 1, 3, 5, 7]
    wm = WaveletMatrix(T)
    # T[1..10) = [4, 5, 5, 2, 7, 5, 6, 1, 3]
    assert wm.range_freq(1, 10, -5, 1000) == 9
    assert wm.range_freq(1, 10, -1, 0) == 0
    assert wm.range_freq(1, 10, 0, 8) == 9
    assert wm.range_freq(1, 10, 10, 10) == 0
    assert wm.range_freq(1, 10, 3, 3) == 0
    assert wm.range_freq(1, 10, 4, 3) == 0


def test_prev_value():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.prev_value(1, 10, 1) is None
    assert wm.prev_value(1, 10, 2) == 1
    assert wm.prev_value(1, 10, 3) == 2
    assert wm.prev_value(1, 10, 4) == 3
    assert wm.prev_value(1, 10, 5) == 4
    assert wm.prev_value(1, 10, 6) == 5
    assert wm.prev_value(1, 10, 7) == 6

    # 変な値を指定したケース
    assert wm.prev_value(1, 10, 10000) == 6
    assert wm.prev_value(-1, 10, 3) == 2
    assert wm.prev_value(1, 10, 0) is None
    assert wm.prev_value(1, 10, -1) is None

    for left, right in combinations(range(len(T)), r=2):
        for upper in range(1, 7):
            actual = wm.prev_value(left, right, upper)

            _T = sorted([t for t in T[left:right] if t < upper])
            if _T:
                expected = _T[-1]
                assert actual == expected
            else:
                assert actual is None


def test_next_value():
    T = [5, 4, 5, 5, 2, 1, 5, 6, 1, 3, 5, 0]
    wm = WaveletMatrix(T)

    # T[1..10) = [4, 5, 5, 2, 1, 5, 6, 1, 3]
    assert wm.next_value(1, 10, 0) == 1
    assert wm.next_value(1, 10, 1) == 1
    assert wm.next_value(1, 10, 2) == 2
    assert wm.next_value(1, 10, 3) == 3
    assert wm.next_value(1, 10, 4) == 4
    assert wm.next_value(1, 10, 5) == 5
    assert wm.next_value(1, 10, 6) == 6
    assert wm.next_value(1, 10, 7) is None

    # 変な値を指定したケース
    assert wm.next_value(1, 10, 10000) is None
    assert wm.next_value(1, 1, 1) is None
    assert wm.next_value(2, 1, 1) is None
    assert wm.next_value(1, 10, -1) == 1

    for left, right in combinations(range(len(T)), r=2):
        for lower in range(8):
            actual = wm.next_value(left, right, lower)
            _T = sorted([t for t in T[left:right] if lower <= t])
            if _T:
                expected = _T[0]
                assert actual == expected
            else:
                assert actual is None
