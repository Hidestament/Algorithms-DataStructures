from src.DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeAdd


def test_propagated_segment():
    A = [1, 3, 2, 6, 5, 4, 7, 9]
    seg = RangeMinimumRangeAdd(A)

    propagated_segment = seg._propagated_segment(1, 7)
    assert propagated_segment == [1, 2, 3, 4, 7]

    propagated_segment = seg._propagated_segment(1, 8)
    assert propagated_segment == [1, 2, 4]

    propagated_segment = seg._propagated_segment(0, 8)
    assert propagated_segment == []

    propagated_segment = seg._propagated_segment(4, 5)
    assert propagated_segment == [1, 3, 6]

    propagated_segment = seg._propagated_segment(0, 7)
    assert propagated_segment == [1, 3, 7]
