from src.DataStructures.Set.multi_set import MultiSet


def test_library_checker_case():
    S = MultiSet()
    for s in [-3, 0, 1, 3]:
        S.insert(s)

    S.insert(3)

    assert S.pop_max() == 3
    assert S.pop_max() == 3

    S.insert(-2)
    S.insert(1)

    assert S.pop_min() == -3
    assert S.pop_min() == -2

    assert S.pop_max() == 1

    assert S.pop_min() == 0

    assert S.pop_max() == 1
