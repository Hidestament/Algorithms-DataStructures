from src.Algorithms.Graph.TopologicalSort.topological_sort import topological_sort


def test_case_aoj():
    graph = [[1], [2], [], [1, 4], [5], [2]]
    indegree = [0, 2, 2, 0, 1, 1]

    assert topological_sort(graph, indegree) == [0, 3, 1, 4, 5, 2]
