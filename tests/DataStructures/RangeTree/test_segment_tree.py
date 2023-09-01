from itertools import combinations

from DataStructures.RangeTree.segment_tree import SegmentTree


def test_min_update():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = SegmentTree(
        N=len(A),
        segfunc=min,
        ide_ele=float("inf"),
    )

    for i, a in enumerate(A):
        seg.update(i, a)

    assert seg.tree == [float("inf"), 2, 2, 6, 3, 2, 6, 8, 3, 5, 2, 11, 9, 6, 20, 8]

    seg.update(5, 1)
    assert seg.tree == [float("inf"), 1, 2, 1, 3, 2, 1, 8, 3, 5, 2, 11, 9, 1, 20, 8]


def test_min_add():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = SegmentTree(
        N=len(A),
        segfunc=min,
        ide_ele=float("inf"),
    )
    for i, a in enumerate(A):
        seg.update(i, a)

    seg.add(5, -5)
    assert seg.tree == [float("inf"), 1, 2, 1, 3, 2, 1, 8, 3, 5, 2, 11, 9, 1, 20, 8]


def test_min_get():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = SegmentTree(
        N=len(A),
        segfunc=min,
        ide_ele=float("inf"),
    )

    for i, a in enumerate(A):
        seg.update(i, a)

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
    seg = SegmentTree(
        N=len(A),
        segfunc=min,
        ide_ele=float("inf"),
    )

    for i, a in enumerate(A):
        seg.update(i, a)

    assert seg.query_recursion(1, 5) == 2

    for left, right in combinations(range(len(A)), 2):
        assert seg.query_recursion(left, right) == min(A[left:right])


def test_min_query():
    A = [3, 5, 2, 11, 9, 6, 20, 8]
    seg = SegmentTree(
        N=len(A),
        segfunc=min,
        ide_ele=float("inf"),
    )

    for i, a in enumerate(A):
        seg.update(i, a)

    assert seg.query(1, 5) == 2
    # A[1:2] = [5]
    assert seg.query(1, 2) == 5

    for left, right in combinations(range(len(A)), 2):
        assert seg.query(left, right) == min(A[left:right])
