from src.Algorithms.Graph.StronglyConnectedComponents.strongly_connected_components import strongly_connected_components


def test_scc():
    graph = [[1], [2], [0, 3], [4], [3, 5, 6], [], []]
    reverse_graph = [[2], [0], [1], [2, 4], [3], [4], [4]]
    scc = strongly_connected_components(graph, reverse_graph)

    assert sorted(scc[0]) == [0, 1, 2]
    assert sorted(scc[1]) == [3, 4]
    assert sorted(scc[2]) == [5]
    assert sorted(scc[3]) == [6]


def test_triangle():
    graph = [[1], [2], [0], [2, 4], [5], [3]]
    reverse_graph = [[2], [0], [1, 3], [5], [3], [4]]
    scc = strongly_connected_components(graph, reverse_graph)

    assert sorted(scc[0]) == [3, 4, 5]
    assert sorted(scc[1]) == [0, 1, 2]


def test_aoj_test_case():
    graph = [[1], [0, 2], [4], [2], [3]]
    reverse_graph = [[1], [0, ], [1, 3], [4], [2]]

    scc = strongly_connected_components(graph, reverse_graph)
    assert sorted(scc[0]) == [0, 1]
    assert sorted(scc[1]) == [2, 3, 4]


def test_sparse():
    graph = [[], [], []]
    reverse_graph = [[], [], []]

    scc = strongly_connected_components(graph, reverse_graph)
    assert scc[0] == [2]
    assert scc[1] == [1]
    assert scc[2] == [0]
