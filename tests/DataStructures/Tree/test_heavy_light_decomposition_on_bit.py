from itertools import product

from DataStructures.Tree.heavy_light_decomposition_on_bit import HeavyLightDecomposition


def brute_force_sum_range(prev, weights, u, v, lca):
    s = 0
    while u != lca:
        s += weights[u]
        u = prev[u]
    while v != lca:
        s += weights[v]
        v = prev[v]

    s += weights[lca]
    return s


def test_sum_range():
    N = 10
    graph = [[1, 4, 8], [0, 2, 3], [1], [1], [0, 5, 7], [4, 6], [5], [4], [0, 9], [8]]
    weights = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    prev = [None, 0, 1, 1, 0, 4, 5, 4, 0, 8]

    hl = HeavyLightDecomposition(graph, weights)

    for i, j in product(range(N), range(N)):
        lca = hl.lowest_common_ancestor(i, j)
        assert hl.vertex_sum(i, j) == brute_force_sum_range(prev, weights, i, j, lca)
