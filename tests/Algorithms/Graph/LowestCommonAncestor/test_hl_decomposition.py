from src.Algorithms.Graph.LowestCommonAncestors.heavy_light_decomposition import (
    HeavyLightDecomposition,
)


def test_lca():
    graph = [[1, 4, 8], [2, 3], [1], [1], [0, 5, 7], [4, 6], [5], [4], [0, 9], [8]]
    hl = HeavyLightDecomposition(graph)

    assert hl.lowest_common_ancestor(0, 3) == 0
    assert hl.lowest_common_ancestor(1, 8) == 0
    assert hl.lowest_common_ancestor(6, 7) == 4
    assert hl.lowest_common_ancestor(5, 7) == 4
    assert hl.lowest_common_ancestor(4, 3) == 0

    # case AOJ GRL_5_C
    graph = [[1, 2, 3], [4, 5], [], [], [], [6, 7], [], []]
    hl = HeavyLightDecomposition(graph)
    assert hl.lowest_common_ancestor(4, 6) == 1
    assert hl.lowest_common_ancestor(4, 7) == 1
    assert hl.lowest_common_ancestor(4, 3) == 0
    assert hl.lowest_common_ancestor(5, 2) == 0

    # case Library Checker
    graph = [[1, 2], [0], [0, 3, 4], [2], [2]]
    hl = HeavyLightDecomposition(graph)
    assert hl.lowest_common_ancestor(0, 1) == 0
    assert hl.lowest_common_ancestor(0, 4) == 0
    assert hl.lowest_common_ancestor(1, 2) == 0
    assert hl.lowest_common_ancestor(2, 3) == 2
    assert hl.lowest_common_ancestor(3, 4) == 2
