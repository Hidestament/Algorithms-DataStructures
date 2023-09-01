from Algorithms.Graph.ShortestPath.dijkstra import dijkstra
from Algorithms.Graph.ShortestPath.reconstruct_shortest_path import reconstruct_shortest_path


def test_tree_no_weight():
    graph = [
        [(1, 1), (2, 1)],
        [(0, 1), (3, 1), (4, 1)],
        [(0, 1), (5, 1), (6, 1), (8, 1)],
        [(1, 1)],
        [(1, 1)],
        [(2, 1)],
        [(2, 1), (7, 1)],
        [(6, 1)],
        [(2, 1)]
    ]
    _, prev = dijkstra(graph, 0)
    shortest_path = reconstruct_shortest_path(prev, 0, 1)
    assert shortest_path == [0, 1]

    shortest_path = reconstruct_shortest_path(prev, 0, 2)
    assert shortest_path == [0, 2]

    shortest_path = reconstruct_shortest_path(prev, 0, 3)
    assert shortest_path == [0, 1, 3]

    shortest_path = reconstruct_shortest_path(prev, 0, 4)
    assert shortest_path == [0, 1, 4]

    shortest_path = reconstruct_shortest_path(prev, 0, 5)
    assert shortest_path == [0, 2, 5]

    shortest_path = reconstruct_shortest_path(prev, 0, 6)
    assert shortest_path == [0, 2, 6]

    shortest_path = reconstruct_shortest_path(prev, 0, 7)
    assert shortest_path == [0, 2, 6, 7]

    shortest_path = reconstruct_shortest_path(prev, 0, 8)
    assert shortest_path == [0, 2, 8]


def test_connected_graph_with_cycle():
    graph = [
        [(1, 7), (2, 4), (3, 3)],
        [(0, 7), (2, 1), (4, 2)],
        [(0, 4), (1, 1), (4, 6)],
        [(0, 3), (4, 5)],
        [(1, 2), (2, 6), (3, 5)]
    ]

    _, prev = dijkstra(graph, 0)
    shortest_path = reconstruct_shortest_path(prev, 0, 1)
    assert shortest_path == [0, 2, 1]

    shortest_path = reconstruct_shortest_path(prev, 0, 2)
    assert shortest_path == [0, 2]

    shortest_path = reconstruct_shortest_path(prev, 0, 3)
    assert shortest_path == [0, 3]

    shortest_path = reconstruct_shortest_path(prev, 0, 4)
    assert shortest_path == [0, 2, 1, 4]
