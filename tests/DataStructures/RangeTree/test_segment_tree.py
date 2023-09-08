from itertools import combinations

from src.DataStructures.RangeTree.segment_tree import (
    RangeMinimumQuery,
    RangeSumQuery,
    RangeCompositeQuery,
)


def test_min_update():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumQuery(A)

    assert seg.data == [10**15, 2, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]

    seg.update(5, 1)
    assert seg.data == [10**15, 1, 2, 1, 3, 2, 1, 8, 3, 5, 2, 11, 9, 1, 20, 8]


def test_sum_update():
    A = [1, 2, 3, 4, 5]
    seg = RangeSumQuery(A)

    assert seg.data == [0, 15, 10, 5, 3, 7, 5, 0, 1, 2, 3, 4, 5, 0, 0, 0]


def test_min_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumQuery(A)

    seg.add(5, -5)
    assert seg.data == [10**15, 1, 2, 1, 3, 2, 1, 8, 3, 5, 2, 11, 9, 1, 20, 8]


def test_min_get():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumQuery(A)

    assert seg.get(0) == 3
    assert seg.get(1) == 5
    assert seg.get(2) == 2
    assert seg.get(3) == 11
    assert seg.get(4) == 9
    assert seg.get(5) == 6
    assert seg.get(6) == 20
    assert seg.get(7) == 8


def test_min_query_recursion():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumQuery(A)

    assert seg.query_recursion(1, 5) == 2
    for left, right in combinations(range(len(A)), 2):
        assert seg.query_recursion(left, right) == min(A[left:right])


def test_min_query():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumQuery(A)

    assert seg.query(1, 5) == 2
    # A[1:2] = [5]
    assert seg.query(1, 2) == 5

    for left, right in combinations(range(len(A)), 2):
        assert seg.query(left, right) == min(A[left:right])


def test_point_set_range_composite_library_checker():
    MOD = 998244353
    A = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    seg = RangeCompositeQuery(A)

    f = seg.query(0, 5)
    x = 11
    assert (f[0] * x + f[1]) % MOD == 14005

    f = seg.query(2, 4)
    x = 12
    assert (f[0] * x + f[1]) % MOD == 470

    seg.update(1, [13, 14])

    f = seg.query(0, 4)
    x = 15
    assert (f[0] * x + f[1]) % MOD == 8275

    f = seg.query(2, 5)
    x = 16
    assert (f[0] * x + f[1]) % MOD == 5500
