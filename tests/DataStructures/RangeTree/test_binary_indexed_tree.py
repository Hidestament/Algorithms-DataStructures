from itertools import combinations

from src.DataStructures.RangeTree.binary_indexed_tree import BinaryIndexedTree


def test_add():
    A = [1, 5, 2, 3, 7, 5, 6, 4]
    bit = BinaryIndexedTree(len(A))

    for i, a in enumerate(A):
        bit.add(i, a)

    assert bit.tree == [
        0,
        A[0],
        A[0] + A[1],
        A[2],
        A[0] + A[1] + A[2] + A[3],
        A[4],
        A[4] + A[5],
        A[6],
        A[0] + A[1] + A[2] + A[3] + A[4] + A[5] + A[6] + A[7],
    ]


def test_sum():
    bit = BinaryIndexedTree(10)

    A = [1, 5, 2, 3, 4, 5, 6, 7, 4, 2]
    for i, a in enumerate(A):
        bit.add(i, a)

    assert bit.sum(-1) == 0
    assert bit.sum(0) == 0
    assert bit.sum(5) == 1 + 5 + 2 + 3 + 4
    assert bit.sum(len(A)) == sum(A)
    assert bit.sum(len(A) + 1) == sum(A)
    assert bit.sum(1000) == sum(A)

    for i in range(1, len(A) + 1):
        assert bit.sum(i) == sum(A[:i])


def test_sum_range():
    bit = BinaryIndexedTree(10)

    A = [1, 5, 2, 3, 4, 5, 6, 7, 4, 2]
    for i, a in enumerate(A):
        bit.add(i, a)

    # A[1..9) = [5, 2, 3, 4, 5, 6, 7, 4]
    assert bit.sum_range(1, 9) == 5 + 2 + 3 + 4 + 5 + 6 + 7 + 4
    assert bit.sum_range(1, 1) == 0
    assert bit.sum_range(1, 0) == 0

    assert bit.sum_range(-1, 10) == sum(A)
    assert bit.sum_range(-10, 1000) == sum(A)

    for i, j in combinations(range(len(A) + 1), r=2):
        assert bit.sum_range(i, j) == sum(A[i:j])


def test_get():
    A = [1, 5, 2, 3, 7, 5, 6, 4]
    bit = BinaryIndexedTree(len(A))

    for i, a in enumerate(A):
        bit.add(i, a)

    assert bit.get(0) == A[0]
    assert bit[0] == A[0]

    assert bit.get(1) == A[1]
    assert bit[1] == A[1]

    assert bit.get(2) == A[2]
    assert bit[2] == A[2]

    for i, a in enumerate(A):
        assert bit.get(i) == a
        assert bit[i] == a


def test_update():
    A = [1, 5, 2, 3, 7, 5, 6, 4]
    bit = BinaryIndexedTree(len(A))

    for i, a in enumerate(A):
        bit.add(i, a)

    for i in range(len(A)):
        bit.update(i, 100)

    assert bit[0] == 100
    assert bit[1] == 100

    for i in range(len(A)):
        assert bit[i] == 100


def test_lower_bound():
    A = [1, 5, 2, 3, 7, 5, 6, 4]
    bit = BinaryIndexedTree(len(A))

    for i, a in enumerate(A):
        bit.add(i, a)

    # A = [1, 5, 2, 3, 7, 5, 6, 4]
    # Sum(A) = [1, 6, 8, 11, 18, 23, 29, 33]
    assert bit.lower_bound(-1) == 0
    assert bit.lower_bound(0) == 0
    assert bit.lower_bound(1) == 1
    assert bit.lower_bound(5) == 2
    assert bit.lower_bound(6) == 2

    # A[0] + A[1] = 1 + 5 = 6
    # A[0] + A[1] + A[2] = 1 + 5 + 2 = 8
    assert bit.lower_bound(7) == 3
    assert bit.lower_bound(8) == 3

    # A[0] + A[1] + A[2] = 1 + 5 + 2 = 8
    # A[0] + A[1] + A[2] + A[3] = 1 + 5 + 2 + 3 = 11
    assert bit.lower_bound(9) == 4
    assert bit.lower_bound(10) == 4
    assert bit.lower_bound(11) == 4

    # A[0] + A[1] + A[2] + A[3] = 1 + 5 + 2 + 3 = 11
    # A[0] + A[1] + A[2] + A[3] + A[4] = 1 + 5 + 2 + 3 + 7 = 18
    assert bit.lower_bound(12) == 5
    assert bit.lower_bound(17) == 5
    assert bit.lower_bound(18) == 5

    # A[0] + A[1] + A[2] + A[3] + A[4] = 1 + 5 + 2 + 3 + 7 = 18
    # A[0] + A[1] + A[2] + A[3] + A[4] + A[5] = 1 + 5 + 2 + 3 + 7 + 5 = 23
    assert bit.lower_bound(19) == 6
    assert bit.lower_bound(22) == 6
    assert bit.lower_bound(23) == 6

    # A[0] + ... + A[5] = 23
    # A[0] + ... + A[5] + A[6] = 23 + 6 = 29
    assert bit.lower_bound(24) == 7
    assert bit.lower_bound(28) == 7
    assert bit.lower_bound(29) == 7

    # A[0] + ... + A[6] = 23 + 6 = 29
    # A[0] + ... + A[6] + A[7] = 23 + 6 + 4 = 33
    assert bit.lower_bound(30) == 8
    assert bit.lower_bound(32) == 8
    assert bit.lower_bound(33) == 8

    assert bit.lower_bound(34) is None
    assert bit.lower_bound(10000) is None
