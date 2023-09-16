import random

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeMinimumQuery


random.seed(1234)


def test_AOJ_test_case1():
    N = 3
    A = [pow(2, 31) - 1 for _ in range(N)]

    treap = RangeMinimumQuery(A)

    treap[0] = 1
    treap[1] = 2
    treap[2] = 3

    assert treap.query(0, 3) == 1
    assert treap.query(1, 3) == 2


def test_AOJ_test_case2():
    A = [pow(2, 31)]

    treap = RangeMinimumQuery(A)
    assert treap.query(0, 1) == pow(2, 31)

    treap[0] = 5

    assert treap.query(0, 1) == 5


def test_AOJ_case2():
    N = 2
    treap = RangeMinimumQuery([2**31 - 1 for _ in range(N)])

    assert treap.query(0, 2) == 2147483647
    assert treap.query(0, 1) == 2147483647
    assert treap.query(1, 2) == 2147483647

    treap[0] = 2

    assert treap.query(0, 2) == 2
    assert treap.query(0, 1) == 2
    assert treap.query(1, 2) == 2147483647

    treap[1] = 1

    assert treap.query(0, 2) == 1
    assert treap.query(0, 1) == 2
    assert treap.query(1, 2) == 1

    treap[1] = 5

    assert treap.query(0, 2) == 2
    assert treap.query(0, 1) == 2
    assert treap.query(1, 2) == 5
