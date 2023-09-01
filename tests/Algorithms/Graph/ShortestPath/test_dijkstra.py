from Algorithms.Graph.ShortestPath.dijkstra import dijkstra


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
    dist, prev = dijkstra(graph, 0)

    assert dist[0] == 0
    assert dist[1] == 1
    assert dist[2] == 1
    assert dist[3] == 2
    assert dist[4] == 2
    assert dist[5] == 2
    assert dist[6] == 2
    assert dist[7] == 3
    assert dist[8] == 2

    assert prev[0] == -1
    assert prev[1] == 0
    assert prev[2] == 0
    assert prev[3] == 1
    assert prev[4] == 1
    assert prev[5] == 2
    assert prev[6] == 2
    assert prev[7] == 6
    assert prev[8] == 2


def test_tree_with_weight():
    graph = [
        [(1, 2), (2, 1)],
        [(0, 2), (3, 5), (4, 1)],
        [(0, 1), (5, 3), (6, 1), (8, 2)],
        [(1, 5)],
        [(1, 1)],
        [(2, 3)],
        [(2, 1), (7, 4)],
        [(6, 4)],
        [(2, 2)]
    ]
    dist, prev = dijkstra(graph, 0)

    assert dist[0] == 0
    assert dist[1] == 2
    assert dist[2] == 1
    assert dist[3] == 7
    assert dist[4] == 3
    assert dist[5] == 4
    assert dist[6] == 2
    assert dist[7] == 6
    assert dist[8] == 3

    assert prev[0] == -1
    assert prev[1] == 0
    assert prev[2] == 0
    assert prev[3] == 1
    assert prev[4] == 1
    assert prev[5] == 2
    assert prev[6] == 2
    assert prev[7] == 6
    assert prev[8] == 2


def test_connected_graph_with_cycle():
    graph = [
        [(1, 7), (2, 4), (3, 3)],
        [(0, 7), (2, 1), (4, 2)],
        [(0, 4), (1, 1), (4, 6)],
        [(0, 3), (4, 5)],
        [(1, 2), (2, 6), (3, 5)]
    ]

    dist, prev = dijkstra(graph, 0)

    assert dist[0] == 0
    assert dist[1] == 5
    assert dist[2] == 4
    assert dist[3] == 3
    assert dist[4] == 7

    assert prev[0] == -1
    assert prev[1] == 2
    assert prev[2] == 0
    assert prev[3] == 0
    assert prev[4] == 1


def test_no_connected_graph():
    graph = [
        [(1, 3), (2, 9)],
        [(0, 3)],
        [(0, 2)],
        [(4, 2)],
        [(3, 2)]
    ]

    dist, prev = dijkstra(graph, 0)

    assert dist[0] == 0
    assert dist[1] == 3
    assert dist[2] == 9
    assert dist[3] == float("INF")
    assert dist[4] == float("INF")

    assert prev[0] == -1
    assert prev[1] == 0
    assert prev[2] == 0
    assert prev[3] == -1
    assert prev[4] == -1
