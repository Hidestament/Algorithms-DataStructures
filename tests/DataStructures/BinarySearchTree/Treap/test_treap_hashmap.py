from src.DataStructures.BinarySearchTree.Treap.treap_hash_map import TreapHashMap


def test_library_checker_case():
    tree = TreapHashMap[int, int]()

    tree[1] = 2
    assert tree[1] == 2
    assert tree.get(2) is None

    tree[2] = 3
    assert tree[1] == 2
    assert tree[2] == 3

    tree[2] = 1
    assert tree[2] == 1
