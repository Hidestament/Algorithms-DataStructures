from src.Algorithms.Graph.CycleDetection.cycle_detection_by_dfs import cycle_detection


def test_undirected_tree_simple():
    graph = [
        [(1, 0)],
        [(0, 0), (2, 1), (3, 2), (5, 3)],
        [(1, 1), (4, 4)],
        [(1, 2)],
        [(2, 4)],
        [(1, 3), (6, 5)],
        [(5, 5)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert path_v == []
    assert path_e == []


def test_undirected_with_cycle_simple():
    # 閉路を含む
    graph = [
        [(1, 0), (5, 1)],
        [(0, 0), (2, 3), (3, 4), (5, 2)],
        [(1, 3), (4, 5)],
        [(1, 4)],
        [(2, 5)],
        [(0, 1), (1, 2)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [0, 1, 5]
    assert sorted(path_e) == [0, 1, 2]

    graph = [
        [(1, 0)],
        [(0, 0), (2, 1), (4, 4)],
        [(1, 1), (3, 2)],
        [(2, 2), (4, 3)],
        [(3, 3), (1, 4)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [1, 2, 3, 4]
    assert sorted(path_e) == [1, 2, 3, 4]

    graph = [
        [(1, 0), (2, 1)],
        [(0, 0), (5, 2), (6, 3)],
        [(0, 1), (3, 4), (4, 5)],
        [(2, 4)],
        [(2, 5)],
        [(1, 2), (6, 6)],
        [(1, 3), (5, 6)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [1, 5, 6]
    assert sorted(path_e) == [2, 3, 6]


def test_directed_with_cycle():
    graph = [
        [(2, 0)],
        [(0, 1)],
        [(14, 2), (3, 3)],
        [(5, 4)],
        [],
        [(6, 5), (9, 6)],
        [(7, 7), (8, 8)],
        [],
        [],
        [(11, 9), (12, 10)],
        [(9, 11)],
        [],
        [(13, 12), (15, 13)],
        [(3, 14)],
        [],
        [],
    ]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [3, 5, 9, 12, 13]
    assert sorted(path_e) == [4, 6, 10, 12, 14]


def test_undirected_path_graph():
    # 0 -e0- 1 -e1- 2 -e2- 3 -e3- 4 -e4- 5
    graph = [
        [(1, 0)],
        [(0, 0), (2, 1)],
        [(1, 1), (3, 2)],
        [(2, 2), (4, 3)],
        [(3, 3), (5, 4)],
        [(4, 4)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert path_v == []
    assert path_e == []


def test_directed_path_graph():
    # 0 -e0-> 1 -e1-> 2 -e2-> 3 -e3-> 4 -e4-> 5
    graph = [[(1, 0)], [(2, 1)], [(3, 2)], [(4, 3)], [(5, 4)], []]
    path_v, path_e = cycle_detection(graph)
    assert path_v == []
    assert path_e == []


def test_undirected_cycle_graph():
    # 0 -e0- 1 -e1- 2 -e2- 3 -e3- 4 -e4- 5 -e5- 0
    graph = [
        [(1, 0), (5, 5)],
        [(0, 0), (2, 1)],
        [(1, 1), (3, 2)],
        [(2, 2), (4, 3)],
        [(3, 3), (5, 4)],
        [(4, 4), (0, 5)],
    ]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [0, 1, 2, 3, 4, 5]
    assert sorted(path_e) == [0, 1, 2, 3, 4, 5]


def test_directed_cycle_graph():
    # 0 -e0-> 1 -e1-> 2 -e2-> 3 -e3-> 4 -e4-> 5 -e5-> 0
    graph = [[(1, 0)], [(2, 1)], [(3, 2)], [(4, 3)], [(5, 4)], [(0, 5)]]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [0, 1, 2, 3, 4, 5]
    assert sorted(path_e) == [0, 1, 2, 3, 4, 5]


def test_undirected_cycle_not_simple():
    graph = [[(1, 0), (1, 1)], [(0, 0), (0, 1)]]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [0, 1]
    assert sorted(path_e) == [0, 1]

    graph = [[(0, 0)]]
    path_v, path_e = cycle_detection(graph)
    assert sorted(path_v) == [0]
    assert sorted(path_e) == [0]
