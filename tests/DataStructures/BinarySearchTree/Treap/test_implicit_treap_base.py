import random
import pytest

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import ImplicitTreap


random.seed(1234)


def _assert_node_information(node):
    if node is None:
        return

    left_subtree_size = node.left.subtree_size if node.left is not None else 0
    right_subtree_size = node.right.subtree_size if node.right is not None else 0

    assert node.subtree_size == left_subtree_size + right_subtree_size + 1

    _assert_node_information(node.left)
    _assert_node_information(node.right)


def test_append():
    treap = ImplicitTreap[int](min, lambda x: x)
    A = [i for i in range(10)]

    for a in A:
        treap.append(a)

    assert treap[0] == 0
    assert treap[1] == 1
    assert treap[2] == 2
    assert treap[3] == 3
    assert treap[4] == 4
    assert treap[5] == 5
    assert treap[6] == 6
    assert treap[7] == 7
    assert treap[8] == 8
    assert treap[9] == 9

    with pytest.raises(IndexError) as _:
        treap[10]

    _assert_node_information(treap.root)


def test_set_items():
    treap = ImplicitTreap[int](min, lambda x: x)
    A = [i for i in range(10)]

    for a in A:
        treap.append(a)

    treap[0] = 10
    treap[1] = 11
    treap[2] = 12
    treap[3] = 13
    treap[4] = 14
    treap[5] = 15
    treap[6] = 16
    treap[7] = 17
    treap[8] = 18
    treap[9] = 19
    _assert_node_information(treap.root)

    assert treap[0] == 10
    assert treap[1] == 11
    assert treap[2] == 12
    assert treap[3] == 13
    assert treap[4] == 14
    assert treap[5] == 15
    assert treap[6] == 16
    assert treap[7] == 17
    assert treap[8] == 18
    assert treap[9] == 19
    with pytest.raises(IndexError) as _:
        treap[10]
    _assert_node_information(treap.root)


def test_pop():
    treap = ImplicitTreap[int](min, lambda x: x)
    A = [0, 1, 2]

    for a in A:
        treap.append(a)
    _assert_node_information(treap.root)

    # A = [1, 2]
    treap.pop(0)
    assert len(treap) == 2
    assert treap[0] == 1
    assert treap[1] == 2
    with pytest.raises(IndexError) as _:
        treap[2]
    _assert_node_information(treap.root)

    # A = [1]
    treap.pop()
    assert len(treap) == 1
    assert treap[0] == 1
    with pytest.raises(IndexError) as _:
        treap[2]
    _assert_node_information(treap.root)

    treap.pop()
    assert len(treap) == 0

    treap = ImplicitTreap[int](min, lambda x: x)
    A = [i for i in range(10)]
    for a in A:
        treap.append(a)
    _assert_node_information(treap.root)

    # A = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    treap.pop(0)
    assert len(treap) == 9
    assert treap[0] == 1
    assert treap[1] == 2
    assert treap[2] == 3
    assert treap[3] == 4
    assert treap[4] == 5
    assert treap[5] == 6
    assert treap[6] == 7
    assert treap[7] == 8
    assert treap[8] == 9
    with pytest.raises(IndexError) as _:
        treap[9]
    _assert_node_information(treap.root)

    # A = [1, 2, 3, 4, 5, 6, 7, 8]
    treap.pop()
    assert len(treap) == 8
    assert treap[0] == 1
    assert treap[1] == 2
    assert treap[2] == 3
    assert treap[3] == 4
    assert treap[4] == 5
    assert treap[5] == 6
    assert treap[6] == 7
    assert treap[7] == 8
    with pytest.raises(IndexError) as _:
        treap[8]
    _assert_node_information(treap.root)

    # A = [1, 2, 3, 5, 6, 7, 8]
    treap.pop(3)
    _assert_node_information(treap.root)
    assert len(treap) == 7
    assert treap[0] == 1
    assert treap[1] == 2
    assert treap[2] == 3
    assert treap[3] == 5
    assert treap[4] == 6
    assert treap[5] == 7
    assert treap[6] == 8
    with pytest.raises(IndexError) as _:
        treap[7]

    # A = [1, 2, 3, 5, 6, 8]
    treap.pop(5)
    _assert_node_information(treap.root)
    assert len(treap) == 6
    assert treap[0] == 1
    assert treap[1] == 2
    assert treap[2] == 3
    assert treap[3] == 5
    assert treap[4] == 6
    assert treap[5] == 8
    with pytest.raises(IndexError) as _:
        treap[6]

    # A = [1, 3, 5, 6, 8]
    treap.pop(1)
    _assert_node_information(treap.root)
    assert len(treap) == 5
    assert treap[0] == 1
    assert treap[1] == 3
    assert treap[2] == 5
    assert treap[3] == 6
    assert treap[4] == 8
    with pytest.raises(IndexError) as _:
        treap[5]

    # A = [1, 3, 5, 6]
    treap.pop()
    _assert_node_information(treap.root)
    assert len(treap) == 4
    assert treap[0] == 1
    assert treap[1] == 3
    assert treap[2] == 5
    assert treap[3] == 6
    with pytest.raises(IndexError) as _:
        treap[4]

    # A = [3, 5, 6]
    treap.pop(0)
    _assert_node_information(treap.root)
    assert len(treap) == 3
    assert treap[0] == 3
    assert treap[1] == 5
    assert treap[2] == 6
    with pytest.raises(IndexError) as _:
        treap[3]
