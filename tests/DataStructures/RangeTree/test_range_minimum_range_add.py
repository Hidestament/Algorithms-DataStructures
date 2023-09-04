from itertools import combinations

from DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeAdd


def test_build_range_minimum_range_add():
    A = [1, 3, 2, 6, 5, 4, 7, 9]
    seg = RangeMinimumRangeAdd(A)
    assert seg.data == [10**15, 1, 1, 4, 1, 2, 4, 7, 1, 3, 2, 6, 5, 4, 7, 9]

    A = [1, 3, 2, 6, 5, 4, 7]
    seg = RangeMinimumRangeAdd(A)
    assert seg.data == [10**15, 1, 1, 4, 1, 2, 4, 7, 1, 3, 2, 6, 5, 4, 7, 10**15]


def test_add_recursion_range_minimum_range_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumRangeAdd(A)

    #             2
    #      2             6
    #   3,    2,     6,     8
    # 3, 5, 2, 11, 9, 6, 20, 8

    #             7
    #      7              11
    #  8       7      11      13
    # 8, 10, 7, 16, 14, 11, 25, 13

    seg.range_update_recursion(0, len(A), 5)
    # A = [8, 10, 7, 16, 14, 11, 25, 13]
    assert seg.data == [10**15, 7, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]
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

    # A = [8, 12, 9, 18, 16, 13, 27, 13]
    seg.range_update_recursion(1, 7, 2)
    assert seg.data == [10**15, 8, 8, 13, 8, 9, 13, 13, 8, 12, 2, 11, 9, 6, 27, 13]
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

    # A = [8, 12, 9, 27, 25, 13, 27, 13]
    seg.range_update_recursion(3, 5, 9)
    assert seg.data == [10**15, 8, 8, 13, 8, 9, 13, 13, 8, 12, 9, 27, 25, 13, 27, 13]
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

    # A = [8, 12, 9, 27, 25, 13, 127, 113]
    seg.range_update_recursion(7, 8, 100)
    seg.range_update_recursion(6, 7, 100)
    assert seg.data == [
        10**15,
        8,
        8,
        13,
        8,
        9,
        13,
        113,
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


def test_add_no_recursion_range_minimum_range_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = RangeMinimumRangeAdd(A)

    #             2
    #      2             6
    #   3,    2,     6,     8
    # 3, 5, 2, 11, 9, 6, 20, 8

    #             7
    #      7              11
    #  8       7      11      13
    # 8, 10, 7, 16, 14, 11, 25, 13

    # seg.range_update(0, len(A), 5)
    # # A = [8, 10, 7, 16, 14, 11, 25, 13]
    # assert seg.data == [10**15, 7, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]
    # assert seg.lazy == [
    #     None,
    #     None,
    #     5,
    #     5,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    # ]

    seg.data = [10**15, 7, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]
    seg.lazy = [
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

    # A = [8, 12, 9, 18, 16, 13, 27, 13]
    seg.range_update(1, 7, 2)
    assert seg.data == [
        1000000000000000,
        8,
        8,
        13,
        8,
        9,
        13,
        13,
        8,
        12,
        2,
        11,
        9,
        6,
        27,
        13,
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
        7,
        7,
        7,
        7,
        None,
        None,
    ]

    # A = [8, 12, 9, 27, 25, 13, 27, 13]
    seg.range_update(3, 5, 9)
    assert seg.data == [10**15, 8, 8, 13, 8, 9, 13, 13, 8, 12, 9, 27, 25, 13, 27, 13]
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

    # A = [8, 12, 9, 27, 25, 13, 127, 113]
    seg.range_update(7, 8, 100)
    seg.range_update(6, 7, 100)
    assert seg.data == [
        10**15,
        8,
        8,
        13,
        8,
        9,
        13,
        113,
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


def test_query_recursion_range_minimum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeAdd(A)

    seg.range_update_recursion(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
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
        seg = RangeMinimumRangeAdd(A)
        assert seg.query_recursion(left, right) == min(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeMinimumRangeAdd(A)
        seg.range_update_recursion(3, 7, 2)
        A = [3, 5, 2, 13, 11, 8, 22, 8]
        assert seg.query_recursion(left, right) == min(A[left:right])


def test_no_query_recursion_range_minimum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeAdd(A)

    seg.range_update(3, 7, 2)

    A = [3, 5, 2, 13, 11, 3, 22, 8]
    assert seg.query(0, len(A)) == min(A)
    assert seg.query(0, 4) == min(A[0:4])
    assert seg.query(4, 8) == min(A[4:8])
    assert seg.query(0, 2) == min(A[0:2])
    assert seg.query(2, 4) == min(A[2:4])
    assert seg.query(4, 6) == min(A[4:6])
    assert seg.query(6, 8) == min(A[6:8])
    assert seg.query(0, 1) == min(A[0:1])
    assert seg.query(1, 2) == min(A[1:2])
    assert seg.query(2, 3) == min(A[2:3])
    assert seg.query(3, 4) == min(A[3:4])
    assert seg.query(4, 5) == min(A[4:5])
    assert seg.query(5, 6) == min(A[5:6])
    assert seg.query(6, 7) == min(A[6:7])
    assert seg.query(7, 8) == min(A[7:8])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeMinimumRangeAdd(A)
        assert seg.query(left, right) == min(A[left:right])

    for left, right in combinations(range(len(A)), r=2):
        A = [3, 5, 2, 11, 9, 6, 20, 8]
        seg = RangeMinimumRangeAdd(A)
        seg.range_update(3, 7, 2)
        A = [3, 5, 2, 13, 11, 8, 22, 8]
        assert seg.query(left, right) == min(A[left:right])


def test_get_range_minimum_range_add():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeAdd(A)

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
    seg = RangeMinimumRangeAdd(A)
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


def test_get_range_minimum_range_add_no_recursion():
    A = [3, 5, 2, 11, 9, 1, 20, 8]
    seg = RangeMinimumRangeAdd(A)

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
    seg = RangeMinimumRangeAdd(A)
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
