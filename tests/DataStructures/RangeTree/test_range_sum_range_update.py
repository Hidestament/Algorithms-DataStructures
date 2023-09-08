from itertools import combinations

from src.DataStructures.RangeTree.lazy_segment_tree import RangeSumRangeUpdate


def test_build_range_sum_range_update():
    A = [1, 3, 2, 6, 5, 4, 7, 9]
    seg = RangeSumRangeUpdate(A)
    assert seg.data == [0, 37, 12, 25, 4, 8, 9, 16, 1, 3, 2, 6, 5, 4, 7, 9]

    A = [1, 3, 2, 6, 5, 4, 7]
    seg = RangeSumRangeUpdate(A)
    assert seg.data == [0, 28, 12, 16, 4, 8, 9, 7, 1, 3, 2, 6, 5, 4, 7, 0]


def test_update_recursion_range_sum_range_update():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeSumRangeUpdate(A)

    #             64
    #     21,           43
    #  8,    13,    15,    28
    # 3, 5, 2, 11, 9, 6, 20, 8

    seg.range_update_recursion(0, len(A), 5)
    # A = [5, 5, 5, 5, 5, 5, 5, 5]
    #            40
    #     20,          20
    #  10,   10,   10    10
    # 5, 5, 5, 5, 5, 5, 5, 5
    assert seg.data == [0, 40, 21, 43, 8, 13, 15, 28, 3, 5, 2, 11, 9, 6, 20, 8]
    assert seg.lazy == [
        None,
        None,
        20,
        20,
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

    seg.range_update_recursion(1, 7, 2)
    # A = [5, 2, 2, 2, 2, 2, 2, 5]
    #            22
    #      11          11
    #   7,    4,   4,     7
    # 5, 2, 2, 2, 2, 2, 2, 5
    assert seg.data == [
        0,
        22,
        11,
        11,
        7,
        4,
        4,
        7,
        5,
        2,
        2,
        11,
        9,
        6,
        2,
        5,
    ]
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

    seg.range_update_recursion(3, 5, 9)
    # A = [5, 2, 2, 9, 9, 2, 2, 5]
    #            36
    #      18          18
    #   7,    11,   11,   7
    # 5, 2, 2, 9, 9, 2, 2, 5
    assert seg.data == [0, 36, 18, 18, 7, 11, 11, 7, 5, 2, 2, 9, 9, 2, 2, 5]
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

    seg.range_update_recursion(6, 7, 8)
    # A = [5, 2, 2, 9, 9, 2, 8, 5]
    #             42
    #     18,          24
    #  7,    11,   11,   13
    # 5, 2, 2, 9, 9, 2, 8, 5
    assert seg.data == [0, 42, 18, 24, 7, 11, 11, 13, 5, 2, 2, 9, 9, 2, 8, 5]
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


def test_update_no_recursion_range_sum_range_update():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeSumRangeUpdate(A)

    #             64
    #     21,           43
    #  8,    13,    15,    28
    # 3, 5, 2, 11, 9, 6, 20, 8

    seg.range_update(0, len(A), 5)
    # A = [5, 5, 5, 5, 5, 5, 5, 5]
    #            40
    #     20,          20
    #  10,   10,   10    10
    # 5, 5, 5, 5, 5, 5, 5, 5
    assert seg.data == [0, 40, 21, 43, 8, 13, 15, 28, 3, 5, 2, 11, 9, 6, 20, 8]
    assert seg.lazy == [
        None,
        None,
        20,
        20,
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

    seg.range_update(1, 7, 2)
    # A = [5, 2, 2, 2, 2, 2, 2, 5]
    #            22
    #      11          11
    #   7,    4,   4,     7
    # 5, 2, 2, 2, 2, 2, 2, 5
    assert seg.data == [
        0,
        22,
        11,
        11,
        7,
        4,
        4,
        7,
        5,
        2,
        2,
        11,
        9,
        6,
        2,
        5,
    ]
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

    seg.range_update(3, 5, 9)
    # A = [5, 2, 2, 9, 9, 2, 2, 5]
    #            36
    #      18          18
    #   7,    11,   11,   7
    # 5, 2, 2, 9, 9, 2, 2, 5
    assert seg.data == [0, 36, 18, 18, 7, 11, 11, 7, 5, 2, 2, 9, 9, 2, 2, 5]
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

    seg.range_update(6, 7, 8)
    # A = [5, 2, 2, 9, 9, 2, 8, 5]
    #             42
    #     18,          24
    #  7,    11,   11,   13
    # 5, 2, 2, 9, 9, 2, 8, 5
    assert seg.data == [0, 42, 18, 24, 7, 11, 11, 13, 5, 2, 2, 9, 9, 2, 8, 5]
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


def test_query_recursion_range_sum_range_update():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeUpdate(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 2, 2, 2, 2, 8]
    assert seg.query_recursion(0, len(A)) == sum(A)
    assert seg.query_recursion(0, 4) == sum(A[0:4])
    assert seg.query_recursion(4, 8) == sum(A[4:8])
    assert seg.query_recursion(0, 2) == sum(A[0:2])
    assert seg.query_recursion(2, 4) == sum(A[2:4])
    assert seg.query_recursion(4, 6) == sum(A[4:6])
    assert seg.query_recursion(6, 8) == sum(A[6:8])
    assert seg.query_recursion(0, 1) == sum(A[0:1])
    assert seg.query_recursion(1, 2) == sum(A[1:2])
    assert seg.query_recursion(2, 3) == sum(A[2:3])
    assert seg.query_recursion(3, 4) == sum(A[3:4])
    assert seg.query_recursion(4, 5) == sum(A[4:5])
    assert seg.query_recursion(5, 6) == sum(A[5:6])
    assert seg.query_recursion(6, 7) == sum(A[6:7])
    assert seg.query_recursion(7, 8) == sum(A[7:8])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeUpdate(A)
        assert seg.query_recursion(left, right) == sum(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeUpdate(A)
        seg.range_update_recursion(3, 7, 2)
        A = [3, 5, 2, 2, 2, 2, 2, 8]
        assert seg.query_recursion(left, right) == sum(A[left:right])


def test_query_no_recursion_range_sum_range_update():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeUpdate(A)

    seg.range_update(3, 7, 2)

    A = [3, 5, 2, 2, 2, 2, 2, 8]
    assert seg.query(0, len(A)) == sum(A)
    assert seg.query(0, 4) == sum(A[0:4])
    assert seg.query(4, 8) == sum(A[4:8])
    assert seg.query(0, 2) == sum(A[0:2])
    assert seg.query(2, 4) == sum(A[2:4])
    assert seg.query(4, 6) == sum(A[4:6])
    assert seg.query(6, 8) == sum(A[6:8])
    assert seg.query(0, 1) == sum(A[0:1])
    assert seg.query(1, 2) == sum(A[1:2])
    assert seg.query(2, 3) == sum(A[2:3])
    assert seg.query(3, 4) == sum(A[3:4])
    assert seg.query(4, 5) == sum(A[4:5])
    assert seg.query(5, 6) == sum(A[5:6])
    assert seg.query(6, 7) == sum(A[6:7])
    assert seg.query(7, 8) == sum(A[7:8])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeUpdate(A)
        assert seg.query(left, right) == sum(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeUpdate(A)
        seg.range_update(3, 7, 2)
        A = [3, 5, 2, 2, 2, 2, 2, 8]
        assert seg.query(left, right) == sum(A[left:right])


def test_get_range_sum_range_update():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeUpdate(A)

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
    seg = RangeSumRangeUpdate(A)
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


def test_get_range_sum_range_update_no_recursion():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeUpdate(A)

    seg.range_update(3, 7, 2)
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
    seg = RangeSumRangeUpdate(A)
    seg.one_point_update(7, 100)
    A = [3, 5, 2, 11, 9, 1, 20, 100]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]
