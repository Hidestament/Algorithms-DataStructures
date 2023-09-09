from src.Algorithms.Graph.StronglyConnectedComponents.strongly_connected_components \
    import strongly_connected_components
from src.Algorithms.Graph.StronglyConnectedComponents.construct import construct


def test_library_checker_case():
    N = 6
    edges = [(1, 4), (5, 2), (3, 0), (5, 5), (4, 1), (0, 3), (4, 2)]
    graph = [[] for _ in range(N)]
    reverse_graph = [[] for _ in range(N)]

    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].append(u)

    scc = strongly_connected_components(graph, reverse_graph)

    assert sorted(scc[0]) == [5]
    assert sorted(scc[1]) == [1, 4]
    assert sorted(scc[2]) == [2]
    assert sorted(scc[3]) == [0, 3]

    scc_graph = construct(graph, scc)
    assert scc_graph[0] == [2]
    assert scc_graph[1] == [2]
    assert scc_graph[2] == []
    assert scc_graph[3] == []

    scc_indegree = [0] * len(scc_graph)
    for u in range(len(scc)):
        for v in scc_graph[u]:
            scc_indegree[v] += 1
    print(f"{scc_indegree=}")
