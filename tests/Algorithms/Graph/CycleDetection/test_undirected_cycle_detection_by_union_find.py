from Algorithms.Graph.CycleDetection.undirected_cycle_detection_by_union_find import (
    undirected_cycle_detection_by_uf,
)


def test_false():
    # Tree
    edges = [(0, 1), (1, 3), (1, 5), (1, 2), (2, 4)]
    assert undirected_cycle_detection_by_uf(6, edges) is False


def test_true():
    # 閉路を含む
    edges = [(4, 2), (2, 1), (3, 1), (1, 5), (0, 1), (5, 0)]
    assert undirected_cycle_detection_by_uf(6, edges) is True


def test_path_graph():
    edges = [(0, 1), (1, 2), (3, 4), (2, 3), (4, 5)]
    assert undirected_cycle_detection_by_uf(6, edges) is False


def test_cycle_graph():
    edges = [(0, 1), (1, 2), (3, 4), (2, 3), (4, 5), (5, 0)]
    assert undirected_cycle_detection_by_uf(6, edges) is True
