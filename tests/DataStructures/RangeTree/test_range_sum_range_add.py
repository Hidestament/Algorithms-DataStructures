from itertools import combinations

from src.DataStructures.RangeTree.lazy_segment_tree import RangeSumRangeAdd


def test_build_range_sum_range_add():
    A = [1, 3, 2, 6, 5, 4, 7, 9]
    seg = RangeSumRangeAdd(A)
    assert seg.data == [0, 37, 12, 25, 4, 8, 9, 16, 1, 3, 2, 6, 5, 4, 7, 9]

    A = [1, 3, 2, 6, 5, 4, 7]
    seg = RangeSumRangeAdd(A)
    assert seg.data == [0, 28, 12, 16, 4, 8, 9, 7, 1, 3, 2, 6, 5, 4, 7, 0]


def test_add_recursion_range_sum_range_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeSumRangeAdd(A)

    #             64
    #      21            43
    #   8,    13,    15,   28
    # 3, 5, 2, 11, 9, 6, 20, 8

    seg.range_update_recursion(0, len(A), 5)
    # A = [8, 10, 7, 16, 14, 11, 25, 13]
    #             104
    #      41             63
    #  18     23      25      38
    # 8, 10, 7, 16, 14, 11, 25, 13
    assert seg.data == [0, 104, 21, 43, 8, 13, 15, 28, 3, 5, 2, 11, 9, 6, 20, 8]
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
    # A = [8, 12, 9, 18, 16, 13, 27, 13]
    #             116
    #      47             69
    #  20     27      29      40
    # 8, 12, 9, 18, 16, 13, 27, 13
    assert seg.data == [0, 116, 47, 69, 20, 27, 29, 40, 8, 12, 2, 11, 9, 6, 27, 13]
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
        7,
        7,
        7,
        7,
        None,
        None,
    ]

    seg.range_update_recursion(3, 5, 9)
    # A = [8, 12, 9, 27, 25, 13, 27, 13]
    #             134
    #      56             78
    #  20     36      38      40
    # 8, 12, 9, 27, 25, 13, 27, 13
    assert seg.data == [0, 134, 56, 78, 20, 36, 38, 40, 8, 12, 9, 27, 25, 13, 27, 13]
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

    seg.range_update_recursion(7, 8, 100)
    seg.range_update_recursion(6, 7, 100)
    # A = [8, 12, 9, 27, 25, 13, 127, 113]
    #             334
    #      56             278
    #  20     36      38      240
    # 8, 12, 9, 27, 25, 13, 127, 113
    assert seg.data == [
        0,
        334,
        56,
        278,
        20,
        36,
        38,
        240,
        8,
        12,
        9,
        27,
        25,
        13,
        127,
        113,
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
        None,
        None,
        None,
        None,
        None,
        None,
    ]


def test_add_no_recursion_range_sum_range_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeSumRangeAdd(A)

    #             64
    #      21            43
    #   8,    13,    15,   28
    # 3, 5, 2, 11, 9, 6, 20, 8

    seg.range_update(0, len(A), 5)

    # A = [8, 10, 7, 16, 14, 11, 25, 13]
    #             104
    #      41             63
    #  18     23      25      38
    # 8, 10, 7, 16, 14, 11, 25, 13
    assert seg.data == [0, 104, 21, 43, 8, 13, 15, 28, 3, 5, 2, 11, 9, 6, 20, 8]
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
    # A = [8, 12, 9, 18, 16, 13, 27, 13]
    #             116
    #      47             69
    #  20     27      29      40
    # 8, 12, 9, 18, 16, 13, 27, 13
    assert seg.data == [0, 116, 47, 69, 20, 27, 29, 40, 8, 12, 2, 11, 9, 6, 27, 13]
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
        7,
        7,
        7,
        7,
        None,
        None,
    ]

    seg.range_update(3, 5, 9)
    # A = [8, 12, 9, 27, 25, 13, 27, 13]
    #             134
    #      56             78
    #  20     36      38      40
    # 8, 12, 9, 27, 25, 13, 27, 13
    assert seg.data == [0, 134, 56, 78, 20, 36, 38, 40, 8, 12, 9, 27, 25, 13, 27, 13]
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

    seg.range_update(7, 8, 100)
    seg.range_update(6, 7, 100)
    # A = [8, 12, 9, 27, 25, 13, 127, 113]
    #             334
    #      56             278
    #  20     36      38      240
    # 8, 12, 9, 27, 25, 13, 127, 113
    assert seg.data == [
        0,
        334,
        56,
        278,
        20,
        36,
        38,
        240,
        8,
        12,
        9,
        27,
        25,
        13,
        127,
        113,
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
        None,
        None,
        None,
        None,
        None,
        None,
    ]


def test_query_recursion_range_sum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
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
        seg = RangeSumRangeAdd(A)
        assert seg.query_recursion(left, right) == sum(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeAdd(A)
        seg.range_update_recursion(3, 7, 2)
        A = [3, 5, 2, 13, 11, 8, 22, 8]
        assert seg.query_recursion(left, right) == sum(A[left:right])


def test_query_no_recursion_range_sum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)

    seg.range_update(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
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
        seg = RangeSumRangeAdd(A)
        assert seg.query(left, right) == sum(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeSumRangeAdd(A)
        seg.range_update(3, 7, 2)
        A = [3, 5, 2, 13, 11, 8, 22, 8]
        assert seg.query(left, right) == sum(A[left:right])


def test_get_range_sum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]

    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)
    seg.one_point_update_recursion(7, 100)

    A = [3, 5, 2, 11, 9, 1, 20, 108]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]


def test_get_range_sum_range_add_no_recursion():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)

    seg.range_update(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]

    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeSumRangeAdd(A)
    seg.one_point_update(7, 100)

    A = [3, 5, 2, 11, 9, 1, 20, 108]
    assert seg.get(0) == A[0]
    assert seg.get(1) == A[1]
    assert seg.get(2) == A[2]
    assert seg.get(3) == A[3]
    assert seg.get(4) == A[4]
    assert seg.get(5) == A[5]
    assert seg.get(6) == A[6]
    assert seg.get(7) == A[7]
