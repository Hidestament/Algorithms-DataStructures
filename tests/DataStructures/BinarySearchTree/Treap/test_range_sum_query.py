import random

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeSumQuery


random.seed(1234)


def test_AOJ_test_case1():
    A = [0, 0, 0]
    treap = RangeSumQuery(A)

    treap.add(0, 1)
    treap.add(1, 2)
    treap.add(2, 3)

    assert treap.query(0, 2) == 3
    assert treap.query(1, 2) == 2
