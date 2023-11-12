from src.DataStructures.DisjointSet.weighted_union_find_tree import WeightedUnionFindTree


def test_AOJ_DSL_1_B():
    uf = WeightedUnionFindTree(5)

    uf.union(0, 2, 5)
    uf.union(1, 2, 3)

    assert uf.diff(0, 1) == 2
    assert uf.diff(1, 3) is None

    uf.union(1, 4, 8)
    assert uf.diff(0, 4) == 10
