import random
from src.DataStructures.BinarySearchTree.Treap.insert_delete_treap import Treap

random.seed(1234)


def test_search():
    tree = Treap()

    tree.insert(2)
    assert len(tree) == 1

    tree.insert(1)
    assert len(tree) == 2

    tree.insert(1)
    assert len(tree) == 3

    tree.insert(3)
    assert len(tree) == 4

    tree.insert(6)
    assert len(tree) == 5

    tree.insert(5)
    assert len(tree) == 6

    tree.insert(7)
    assert len(tree) == 7

    assert tree.search(1).key == 1
    assert tree.search(1).count == 2

    assert tree.search(2).key == 2
    assert tree.search(2).count == 1

    assert tree.search(3).key == 3
    assert tree.search(3).count == 1

    assert tree.search(4) is None

    assert tree.search(5).key == 5
    assert tree.search(5).count == 1

    assert tree.search(6).key == 6
    assert tree.search(6).count == 1

    assert tree.search(7).key == 7
    assert tree.search(7).count == 1

    assert tree.search(8) is None


def test_count():
    tree = Treap()

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.count(1) == 2
    assert tree.count(2) == 1
    assert tree.count(3) == 1
    assert tree.count(4) == 0
    assert tree.count(5) == 1
    assert tree.count(6) == 1
    assert tree.count(7) == 1
    assert tree.count(8) == 0


def test_min_element():
    tree = Treap()

    assert tree.min_element() is None

    tree.insert(100000)
    assert len(tree) == 1
    assert tree.min_element().key == 100000

    tree.insert(2)
    assert len(tree) == 2

    tree.insert(1)
    assert len(tree) == 3

    tree.insert(1)
    assert len(tree) == 4
    tree.insert(3)
    assert len(tree) == 5

    tree.insert(6)
    assert len(tree) == 6

    tree.insert(5)
    assert len(tree) == 7

    tree.insert(7)
    assert len(tree) == 8

    assert tree.min_element().key == 1
    assert tree.min_element().count == 2


def test_max_element():
    tree = Treap()

    assert tree.max_element() is None

    tree.insert(-100000)
    assert tree.max_element().key == -100000

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.max_element().key == 7
    assert tree.max_element().count == 1


def test_lower_bound():
    tree = Treap()
    assert tree.lower_bound(1) is None

    tree.insert(100000)
    assert tree.lower_bound(100000).key == 100000
    assert tree.lower_bound(100000 - 1).key == 100000
    assert tree.lower_bound(100000 + 1) is None

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.lower_bound(-1).key == 1
    assert tree.lower_bound(0).key == 1
    assert tree.lower_bound(1).key == 1
    assert tree.lower_bound(2).key == 2
    assert tree.lower_bound(3).key == 3
    assert tree.lower_bound(4).key == 5
    assert tree.lower_bound(5).key == 5
    assert tree.lower_bound(6).key == 6
    assert tree.lower_bound(7).key == 7
    assert tree.lower_bound(8).key == 100000
    assert tree.lower_bound(100000).key == 100000
    assert tree.lower_bound(100000 - 1).key == 100000
    assert tree.lower_bound(100000 + 1) is None


def test_upper_bound():
    tree = Treap()
    assert tree.upper_bound(1) is None

    tree.insert(-100000)
    assert tree.upper_bound(-100000 - 1) is None
    assert tree.upper_bound(-100000).key == -100000
    assert tree.upper_bound(-100000 + 1).key == -100000

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.upper_bound(-100000 - 1) is None
    assert tree.upper_bound(-100000).key == -100000
    assert tree.upper_bound(0).key == -100000
    assert tree.upper_bound(1).key == 1
    assert tree.upper_bound(2).key == 2
    assert tree.upper_bound(3).key == 3
    assert tree.upper_bound(4).key == 3
    assert tree.upper_bound(5).key == 5
    assert tree.upper_bound(6).key == 6
    assert tree.upper_bound(7).key == 7
    assert tree.upper_bound(8).key == 7


def test_inorder():
    tree = Treap()
    tree.insert(-100000)
    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(100000)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    inorder = [i.key for i in tree.inorder()]
    assert inorder == [-100000, 1, 2, 3, 5, 6, 7, 100000]


def test_delete():
    tree = Treap()
    tree.insert(2)
    tree.delete(2)
    assert tree.root is None
    assert [i.key for i in tree.inorder()] == []

    tree = Treap()
    tree.insert(-100000)
    tree.insert(2)
    tree.insert(2)
    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(100000)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    # [1, 1, 2, 2, 2, 3, 5, 6, 7, 10000]
    tree.delete(-100000)
    assert tree.search(-100000) is None
    assert [i.key for i in tree.inorder()] == [1, 2, 3, 5, 6, 7, 100000]

    # [1, 1, 2, 2, 2, 3, 5, 6, 7]
    tree.delete(100000)
    assert tree.search(100000) is None
    assert [i.key for i in tree.inorder()] == [1, 2, 3, 5, 6, 7]

    # [2, 2, 2, 3, 5, 6, 7]
    tree.delete(1, 2)
    assert tree.search(1) is None
    assert [i.key for i in tree.inorder()] == [2, 3, 5, 6, 7]

    # [2, 2, 3, 5, 6, 7]
    tree.delete(2, 1)
    assert tree.search(2).key == 2
    assert tree.search(2).count == 2
    assert [i.key for i in tree.inorder()] == [2, 3, 5, 6, 7]

    # [2, 5, 6, 7]
    tree.delete(3)
    assert tree.search(3) is None
    assert [i.key for i in tree.inorder()] == [2, 5, 6, 7]

    tree.delete(4)
    assert [i.key for i in tree.inorder()] == [2, 5, 6, 7]

    # [2, 6, 7]
    tree.delete(5)
    assert tree.delete(5) is None
    assert [i.key for i in tree.inorder()] == [2, 6, 7]

    # [2, 7]
    tree.delete(6)
    assert tree.search(6) is None
    assert [i.key for i in tree.inorder()] == [2, 7]

    # [2]
    tree.delete(7)
    assert tree.search(7) is None
    assert [i.key for i in tree.inorder()] == [2]

    tree.delete(8)
    assert tree.delete(8) is None
    assert [i.key for i in tree.inorder()] == [2]


def test_kth_smallest_element():
    tree = Treap()
    tree.insert(-100000)
    tree.insert(2)
    tree.insert(2)
    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(100000)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    A = [-100000, 1, 1, 2, 2, 2, 3, 5, 6, 7, 100000]

    for k, a in enumerate(A, start=1):
        assert tree.kth_smallest_element(k).key == a
    assert tree.kth_smallest_element(15) is None

    tree.delete(2, 3)
    tree.delete(1, 1)
    tree.delete(100000)

    assert [node.key for node in tree.inorder()] == [-100000, 1, 3, 5, 6, 7]

    print(f"{tree.root=}")

    A = [-100000, 1, 3, 5, 6, 7]
    for k, a in enumerate(A, start=1):
        assert tree.kth_smallest_element(k).key == a


def test_AOJ_binary_search_tree_1():
    tree = Treap()
    tree.insert(30)
    tree.insert(88)
    tree.insert(12)
    tree.insert(1)
    tree.insert(20)
    tree.insert(17)
    tree.insert(25)

    assert [node.key for node in tree.inorder()] == [1, 12, 17, 20, 25, 30, 88]


def test_AOJ_binary_search_tree_2():
    tree = Treap()
    tree.insert(30)
    tree.insert(88)
    tree.insert(12)
    tree.insert(1)
    tree.insert(20)

    assert 12 in tree

    tree.insert(17)
    tree.insert(25)

    assert 16 not in tree

    assert [node.key for node in tree.inorder()] == [1, 12, 17, 20, 25, 30, 88]


def test_AOJ_binary_search_tree_3():
    tree = Treap()
    tree.insert(8)
    tree.insert(2)
    tree.insert(3)
    tree.insert(7)
    tree.insert(22)
    tree.insert(1)

    assert 1 in tree
    assert 2 in tree
    assert 3 in tree

    assert 4 not in tree
    assert 5 not in tree
    assert 6 not in tree

    assert 7 in tree
    assert 8 in tree

    assert [node.key for node in tree.inorder()] == [1, 2, 3, 7, 8, 22]

    tree.delete(3)
    tree.delete(7)

    assert [node.key for node in tree.inorder()] == [1, 2, 8, 22]


def test_AOJ_binary_search_tree_3_case3():
    tree = Treap()
    tree.insert(30)
    tree.insert(17)
    tree.insert(88)
    tree.insert(53)
    tree.insert(5)
    tree.insert(20)
    tree.insert(18)
    tree.insert(28)
    tree.insert(27)
    tree.insert(60)
    assert [node.key for node in tree.inorder()] == [5, 17, 18, 20, 27, 28, 30, 53, 60, 88]

    assert -1 not in tree
    assert 2 not in tree
    assert 3 not in tree
    assert 4 not in tree

    assert 5 in tree

    assert 6 not in tree
    assert 10 not in tree

    assert 17 in tree
    assert 28 in tree

    assert 29 not in tree

    assert 30 in tree

    assert 31 not in tree
    assert 50 not in tree
    assert 51 not in tree
    assert 52 not in tree

    assert 53 in tree

    assert 54 not in tree

    assert 60 in tree
    assert 88 in tree

    assert 89 not in tree

    tree.insert(2000000000)
    tree.insert(55)
    tree.insert(63)
    tree.insert(-1)
    tree.insert(8)
    assert [node.key for node in tree.inorder()] == [-1, 5, 8, 17, 18, 20, 27, 28, 30, 53, 55, 60, 63, 88, 2000000000]

    tree.delete(53)
    tree.delete(2000000000)
    tree.delete(20)

    tree.delete(5)
    tree.delete(8)
    assert [node.key for node in tree.inorder()] == [-1, 17, 18, 27, 28, 30, 55, 60, 63, 88]


def test_AOJ_heap_test_case():
    tree = Treap()

    tree.insert(35)
    tree.insert(3)
    tree.insert(1)
    tree.insert(14)
    tree.insert(80)
    tree.insert(42)
    tree.insert(86)
    tree.insert(21)
    tree.insert(7)
    tree.insert(6)

    assert [node.key for node in tree.inorder()] == [1, 3, 6, 7, 14, 21, 35, 42, 80, 86]

    assert 21 in tree
    assert 22 not in tree

    tree.delete(35)
    tree.delete(99)

    assert [node.key for node in tree.inorder()] == [1, 3, 6, 7, 14, 21, 42, 80, 86]
