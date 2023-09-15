from src.DataStructures.BinarySearchTree.binary_search_tree import BinarySearchTree


def test_search():
    tree = BinarySearchTree()

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

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
    tree = BinarySearchTree()

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
    tree = BinarySearchTree()

    assert tree.min_element() is None

    tree.insert(100000)
    assert tree.min_element().key == 100000

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.min_element().key == 1
    assert tree.min_element().count == 2


def test_max_element():
    tree = BinarySearchTree()

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


def test_successor():
    tree = BinarySearchTree()
    assert tree.successor(1) is None

    tree.insert(100000)
    assert tree.successor(100000) is None

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.successor(0) is None
    assert tree.successor(1).key == 2
    assert tree.successor(2).key == 3
    assert tree.successor(3).key == 5
    assert tree.successor(4) is None
    assert tree.successor(5).key == 6
    assert tree.successor(6).key == 7
    assert tree.successor(7).key == 100000
    assert tree.successor(100000) is None


def test_predecessor():
    tree = BinarySearchTree()
    assert tree.predecessor(1) is None

    tree.insert(-100000)
    assert tree.predecessor(-100000) is None

    tree.insert(2)
    tree.insert(1)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    assert tree.predecessor(-100000) is None
    assert tree.predecessor(0) is None
    assert tree.predecessor(1).key == -100000
    assert tree.predecessor(2).key == 1
    assert tree.predecessor(3).key == 2
    assert tree.predecessor(4) is None
    assert tree.predecessor(5).key == 3
    assert tree.predecessor(6).key == 5
    assert tree.predecessor(7).key == 6
    assert tree.predecessor(8) is None


def test_inorder():
    tree = BinarySearchTree()
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
    tree = BinarySearchTree()
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

    tree.delete(-100000)
    assert tree.search(-100000) is None

    tree.delete(100000)
    assert tree.search(100000) is None

    tree.delete(1, 2)
    assert tree.search(1) is None

    tree.delete(2, 1)
    assert tree.search(2).key == 2
    assert tree.search(2).count == 2

    tree.delete(3)
    assert tree.search(3) is None

    tree.delete(4)
    tree.delete(5)
    assert tree.delete(5) is None
    tree.delete(6)
    assert tree.search(6) is None
    tree.delete(7)
    assert tree.search(7) is None
    tree.delete(8)
    assert tree.delete(8) is None


def test_kth_smallest_element():
    tree = BinarySearchTree()
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
    A = [-100000, 1, 3, 5, 6, 7]
    for k, a in enumerate(A, start=1):
        assert tree.kth_smallest_element(k).key == a


def test_AOJ_binary_search_tree_1():
    tree = BinarySearchTree()
    tree.insert(30)
    tree.insert(88)
    tree.insert(12)
    tree.insert(1)
    tree.insert(20)
    tree.insert(17)
    tree.insert(25)

    assert [node.key for node in tree.inorder()] == [1, 12, 17, 20, 25, 30, 88]
    assert [node.key for node in tree.preorder()] == [30, 12, 1, 20, 17, 25, 88]


def test_AOJ_binary_search_tree_2():
    tree = BinarySearchTree()
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
    assert [node.key for node in tree.preorder()] == [30, 12, 1, 20, 17, 25, 88]


def test_AOJ_binary_search_tree_3():
    tree = BinarySearchTree()
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
    assert [node.key for node in tree.preorder()] == [8, 2, 1, 3, 7, 22]

    tree.delete(3)
    tree.delete(7)

    assert [node.key for node in tree.inorder()] == [1, 2, 8, 22]
    assert [node.key for node in tree.preorder()] == [8, 2, 1, 22]


def test_AOJ_binary_search_tree_3_case3():
    tree = BinarySearchTree()
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
    assert [node.key for node in tree.preorder()] == [30, 17, 5, 20, 18, 28, 27, 88, 53, 60]

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
    assert [node.key for node in tree.preorder()] == [30, 17, 5, -1, 8, 20, 18, 28, 27, 88, 53, 60, 55, 63, 2000000000]

    tree.delete(53)
    tree.delete(2000000000)
    tree.delete(20)

    tree.delete(5)
    tree.delete(8)
    assert [node.key for node in tree.inorder()] == [-1, 17, 18, 27, 28, 30, 55, 60, 63, 88]
    assert [node.key for node in tree.preorder()] == [30, 17, -1, 27, 18, 28, 88, 60, 55, 63]
