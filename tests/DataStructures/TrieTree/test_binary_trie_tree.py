from src.DataStructures.TrieTree.binary_trie_tree import BinaryTrie


def test_count():
    tree = BinaryTrie()

    tree.insert(0)

    tree.insert(15)
    tree.insert(15)
    tree.insert(15)

    tree.insert(16)
    tree.insert(16)
    tree.insert(16)
    tree.insert(16)
    tree.insert(16)

    tree.insert(30)

    for i in range(35):
        if i == 0:
            assert tree.count(i) == 1
        elif i == 15:
            assert tree.count(i) == 3
        elif i == 16:
            assert tree.count(i) == 5
        elif i == 30:
            assert tree.count(i) == 1
        else:
            assert tree.count(i) == 0


def test_contains():
    tree = BinaryTrie()

    tree.insert(0)

    tree.insert(15)
    tree.insert(15)
    tree.insert(15)

    tree.insert(16)
    tree.insert(16)
    tree.insert(16)
    tree.insert(16)
    tree.insert(16)

    tree.insert(30)

    for i in range(35):
        if i == 0:
            assert i in tree
        elif i == 15:
            assert i in tree
        elif i == 16:
            assert i in tree
        elif i == 30:
            assert i in tree
        else:
            assert i not in tree


def test_discard():
    tree = BinaryTrie()

    tree.insert(0)

    tree.insert(15)
    tree.insert(15)
    tree.insert(15)

    tree.discard(0)
    assert 0 not in tree

    tree.discard(1)
    assert 1 not in tree

    tree.discard(15)
    assert 15 in tree
    tree.discard(15)
    assert 15 in tree
    tree.discard(15)
    assert 15 not in tree


def test_len():
    tree = BinaryTrie()
    assert len(tree) == 0

    tree.insert(0)
    assert len(tree) == 1

    tree.insert(15)
    assert len(tree) == 2
    tree.insert(15)
    assert len(tree) == 3
    tree.insert(15)
    assert len(tree) == 4

    tree.insert(16)
    assert len(tree) == 5
    tree.insert(16)
    assert len(tree) == 6
    tree.insert(16)
    assert len(tree) == 7
    tree.insert(16)
    assert len(tree) == 8
    tree.insert(16)
    assert len(tree) == 9
    tree.insert(30)
    assert len(tree) == 10


def test_get_min_element():
    tree = BinaryTrie()

    tree.insert(5)

    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)

    assert tree.get_min_element() == 5

    # '0b1110
    tree.discard(5)
    assert tree.get_min_element() == 14

    tree.discard(14)
    assert tree.get_min_element() == 15

    tree.discard(15)
    tree.discard(15)
    assert tree.get_min_element() == 15

    tree.discard(15)
    assert tree.get_min_element() == 16

    tree.discard(16)
    assert tree.get_min_element() is None


def test_get_max_element():
    tree = BinaryTrie()

    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)
    tree.insert(30)
    tree.insert(30)
    tree.insert(35)

    assert tree.get_max_element() == 35

    # '0b1110
    tree.discard(35)
    assert tree.get_max_element() == 30

    tree.discard(30)
    assert tree.get_max_element() == 30

    tree.discard(30)
    assert tree.get_max_element() == 16

    tree.discard(16)
    assert tree.get_max_element() == 15

    tree.discard(15)
    assert tree.get_max_element() == 15

    tree.discard(15)
    assert tree.get_max_element() == 15

    tree.discard(15)
    assert tree.get_max_element() == 14

    tree.discard(14)
    assert tree.get_max_element() == 5

    tree.discard(5)
    assert tree.get_max_element() is None


def test_pop_min_element():
    tree = BinaryTrie()

    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)

    assert tree.pop_min_element() == 5
    assert tree.pop_min_element() == 14
    assert tree.pop_min_element() == 15
    assert tree.pop_min_element() == 15
    assert tree.pop_min_element() == 15
    assert tree.pop_min_element() == 16
    assert tree.pop_min_element() is None


def test_pop_max_element():
    tree = BinaryTrie()

    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)
    tree.insert(30)
    tree.insert(30)
    tree.insert(35)

    assert tree.pop_max_element() == 35
    assert tree.pop_max_element() == 30
    assert tree.pop_max_element() == 30
    assert tree.pop_max_element() == 16
    assert tree.pop_max_element() == 15
    assert tree.pop_max_element() == 15
    assert tree.pop_max_element() == 15
    assert tree.pop_max_element() == 14
    assert tree.pop_max_element() == 5
    assert tree.pop_max_element() is None


def test_get_kth_smallest_element():
    tree = BinaryTrie()

    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)

    assert tree.get_kth_smallest_element(1) == 5
    assert tree.get_kth_smallest_element(2) == 14
    assert tree.get_kth_smallest_element(3) == 15
    assert tree.get_kth_smallest_element(4) == 15
    assert tree.get_kth_smallest_element(5) == 15
    assert tree.get_kth_smallest_element(6) == 16
    assert tree.get_kth_smallest_element(7) is None


def test_get_kth_largest_element():
    tree = BinaryTrie()

    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(15)
    tree.insert(15)
    tree.insert(16)
    tree.insert(30)
    tree.insert(30)
    tree.insert(35)

    assert tree.get_kth_largest_element(1) == 35
    assert tree.get_kth_largest_element(2) == 30
    assert tree.get_kth_largest_element(3) == 30
    assert tree.get_kth_largest_element(4) == 16
    assert tree.get_kth_largest_element(5) == 15
    assert tree.get_kth_largest_element(6) == 15
    assert tree.get_kth_largest_element(7) == 15
    assert tree.get_kth_largest_element(8) == 14
    assert tree.get_kth_largest_element(9) == 5
    assert tree.get_kth_largest_element(10) is None


def test_get_min_element_xor():
    tree = BinaryTrie()

    # '0b101'
    tree.insert(5)
    # '0b1110'
    tree.insert(14)
    # '0b1111'
    tree.insert(15)
    # '0b10000'
    tree.insert(16)
    # '0b11110'
    tree.insert(30)
    # '0b100011'
    tree.insert(35)

    for x in range(40):
        xor = [(5 ^ x, 5), (14 ^ x, 14), (15 ^ x, 15), (16 ^ x, 16), (30 ^ x, 30), (35 ^ x, 35)]
        min_xor = min(xor, key=lambda x: x[0])
        assert tree.get_min_element_xor(x) == min_xor[1]


def test_get_max_element_xor():
    tree = BinaryTrie()

    # '0b101'
    tree.insert(5)
    # '0b1110'
    tree.insert(14)
    # '0b1111'
    tree.insert(15)
    # '0b10000'
    tree.insert(16)
    # '0b11110'
    tree.insert(30)
    # '0b100011'
    tree.insert(35)

    for x in range(40):
        xor = [(5 ^ x, 5), (14 ^ x, 14), (15 ^ x, 15), (16 ^ x, 16), (30 ^ x, 30), (35 ^ x, 35)]
        max_xor = max(xor, key=lambda x: x[0])
        assert tree.get_max_element_xor(x) == max_xor[1]


def test_get_kth_smallest_element_xor():
    tree = BinaryTrie()

    tree.insert(1)
    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(16)
    tree.insert(30)
    tree.insert(30)
    tree.insert(35)
    tree.insert(40)
    tree.insert(42)

    for x in range(50):
        xor = [(1 ^ x, 1), (5 ^ x, 5), (14 ^ x, 14), (15 ^ x, 15), (16 ^ x, 16),
               (30 ^ x, 30), (30 ^ x, 30), (35 ^ x, 35), (40 ^ x, 40), (42 ^ x, 42)]
        xor.sort(key=lambda x: x[0])

        assert tree.get_kth_smallest_element_xor(x, 1) == xor[0][1]
        assert tree.get_kth_smallest_element_xor(x, 2) == xor[1][1]
        assert tree.get_kth_smallest_element_xor(x, 3) == xor[2][1]
        assert tree.get_kth_smallest_element_xor(x, 4) == xor[3][1]
        assert tree.get_kth_smallest_element_xor(x, 5) == xor[4][1]
        assert tree.get_kth_smallest_element_xor(x, 6) == xor[5][1]
        assert tree.get_kth_smallest_element_xor(x, 7) == xor[6][1]
        assert tree.get_kth_smallest_element_xor(x, 8) == xor[7][1]
        assert tree.get_kth_smallest_element_xor(x, 9) == xor[8][1]
        assert tree.get_kth_smallest_element_xor(x, 10) == xor[9][1]
        assert tree.get_kth_smallest_element_xor(x, 11) is None


def test_get_kth_largest_element_xor():
    tree = BinaryTrie()

    tree.insert(1)
    tree.insert(5)
    tree.insert(14)
    tree.insert(15)
    tree.insert(16)
    tree.insert(30)
    tree.insert(30)
    tree.insert(35)
    tree.insert(40)
    tree.insert(42)

    for x in range(50):
        xor = [(1 ^ x, 1), (5 ^ x, 5), (14 ^ x, 14), (15 ^ x, 15), (16 ^ x, 16),
               (30 ^ x, 30), (30 ^ x, 30), (35 ^ x, 35), (40 ^ x, 40), (42 ^ x, 42)]
        xor.sort(key=lambda x: x[0], reverse=True)

        assert tree.get_kth_largest_element_xor(x, 1) == xor[0][1]
        assert tree.get_kth_largest_element_xor(x, 2) == xor[1][1]
        assert tree.get_kth_largest_element_xor(x, 3) == xor[2][1]
        assert tree.get_kth_largest_element_xor(x, 4) == xor[3][1]
        assert tree.get_kth_largest_element_xor(x, 5) == xor[4][1]
        assert tree.get_kth_largest_element_xor(x, 6) == xor[5][1]
        assert tree.get_kth_largest_element_xor(x, 7) == xor[6][1]
        assert tree.get_kth_largest_element_xor(x, 8) == xor[7][1]
        assert tree.get_kth_largest_element_xor(x, 9) == xor[8][1]
        assert tree.get_kth_largest_element_xor(x, 10) == xor[9][1]
        assert tree.get_kth_largest_element_xor(x, 11) is None
