from itertools import combinations

from DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeUpdate


def test_build_range_minimum_range_update():
    A = [1, 3, 2, 6, 5, 4, 7, 9]
    seg = RangeMinimumRangeUpdate(A)
    assert seg.data == [10**15, 1, 1, 4, 1, 2, 4, 7, 1, 3, 2, 6, 5, 4, 7, 9]

    A = [1, 3, 2, 6, 5, 4, 7]
    seg = RangeMinimumRangeUpdate(A)
    assert seg.data == [10**15, 1, 1, 4, 1, 2, 4, 7, 1, 3, 2, 6, 5, 4, 7, 10**15]


def test_update_recursion_range_minimum_range_update():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumRangeUpdate(A)

    seg.range_update_recursion(0, len(A), 5)
    assert seg.data == [10**15, 5, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]
    assert seg.lazy == [
        None,
        None,
        5,
        5,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    # A = [5, 2, 2, 2, 2, 2, 2, 5]
    seg.range_update_recursion(1, 7, 2)
    assert seg.data == [10**15, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 11, 9, 6, 2, 5]
    assert seg.lazy == [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        2,
        2,
        2,
        2,
        None,
        None,
    ]

    # A = [5, 2, 2, 9, 9, 2, 2, 5]
    seg.range_update_recursion(3, 5, 9)
    assert seg.data == [10**15, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 9, 9, 2, 2, 5]
    assert seg.lazy == [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    # A = [5, 2, 2, 9, 9, 2, 8, 5]
    seg.range_update_recursion(6, 7, 8)
    assert seg.data == [10**15, 2, 2, 2, 2, 2, 2, 5, 5, 2, 2, 9, 9, 2, 8, 5]
    assert seg.lazy == [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]


def test_query_recursion_range_minimum_range_update():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeUpdate(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 2, 2, 2, 2, 8]
    assert seg.query_recursion(0, len(A)) == min(A)
    assert seg.query_recursion(0, 4) == min(A[0:4])
    assert seg.query_recursion(4, 8) == min(A[4:8])
    assert seg.query_recursion(0, 2) == min(A[0:2])
    assert seg.query_recursion(2, 4) == min(A[2:4])
    assert seg.query_recursion(4, 6) == min(A[4:6])
    assert seg.query_recursion(6, 8) == min(A[6:8])
    assert seg.query_recursion(0, 1) == min(A[0:1])
    assert seg.query_recursion(1, 2) == min(A[1:2])
    assert seg.query_recursion(2, 3) == min(A[2:3])
    assert seg.query_recursion(3, 4) == min(A[3:4])
    assert seg.query_recursion(4, 5) == min(A[4:5])
    assert seg.query_recursion(5, 6) == min(A[5:6])
    assert seg.query_recursion(6, 7) == min(A[6:7])
    assert seg.query_recursion(7, 8) == min(A[7:8])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeMinimumRangeUpdate(A)
        assert seg.query_recursion(left, right) == min(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeMinimumRangeUpdate(A)
        seg.range_update_recursion(3, 7, 2)
        A = [3, 5, 2, 2, 2, 2, 2, 8]
        assert seg.query_recursion(left, right) == min(A[left:right])


def test_get_range_minimum_range_update():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeUpdate(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 2, 2, 2, 2, 8]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]

    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeUpdate(A)
    seg.one_point_update_recursion(7, 100)

    A = [3, 5, 2, 11, 9, 1, 20, 100]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]
