from DataStructures.RangeTree.lazy_segment_tree import (
    RangeSumRangeAffine,
    PointGetRangeAffineWithMod,
)


def test_range_affine_point_get_library_checker():
    A = [1, 2, 3, 4, 5]
    MOD = 998244353
    seg = PointGetRangeAffineWithMod(A, MOD)
    seg.range_update_recursion(2, 4, [100, 101])
    assert seg.get(0) == 1
    assert seg.get(1) == 2
    assert seg.get(2) == 401
    assert seg.get(3) == 501
    assert seg.get(4) == 5

    seg.range_update_recursion(1, 3, [102, 103])
    assert seg.get(0) == 1
    assert seg.get(1) == 307
    assert seg.get(2) == 41005
    assert seg.get(3) == 501
    assert seg.get(4) == 5


def test_range_affine_point_get_library_checker_no_recursion():
    A = [1, 2, 3, 4, 5]
    MOD = 998244353
    seg = PointGetRangeAffineWithMod(A, MOD)
    seg.range_update(2, 4, [100, 101])
    assert seg.get(0) == 1
    assert seg.get(1) == 2
    assert seg.get(2) == 401
    assert seg.get(3) == 501
    assert seg.get(4) == 5

    seg.range_update(1, 3, [102, 103])
    assert seg.get(0) == 1
    assert seg.get(1) == 307
    assert seg.get(2) == 41005
    assert seg.get(3) == 501
    assert seg.get(4) == 5


def test_range_affine_range_sum_library_checker():
    A = [1, 2, 3, 4, 5]
    seg = RangeSumRangeAffine(A)

    assert seg.query_recursion(0, 5) == 15

    seg.range_update_recursion(2, 4, [100, 101])
    assert seg.query_recursion(0, 3) == 404

    seg.range_update_recursion(1, 3, [102, 103])
    assert seg.query_recursion(2, 5) == 41511

    seg.range_update_recursion(2, 5, [104, 105])
    assert seg.query_recursion(0, 5) == 4317767


def test_range_affine_range_sum_library_checker_no_recursion():
    A = [1, 2, 3, 4, 5]
    seg = RangeSumRangeAffine(A)

    assert seg.query(0, 5) == 15

    seg.range_update(2, 4, [100, 101])
    assert seg.query(0, 3) == 404

    seg.range_update(1, 3, [102, 103])
    assert seg.query(2, 5) == 41511

    seg.range_update(2, 5, [104, 105])
    assert seg.query(0, 5) == 4317767
