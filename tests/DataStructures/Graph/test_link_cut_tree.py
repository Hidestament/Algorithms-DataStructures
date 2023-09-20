from src.DataStructures.Graph.link_cut_tree import LinkCutTree


def test_link():
    N = 5
    P = [0, 0, 2, 2]

    graph = [[] for _ in range(N)]
    for i, p in enumerate(P, start=1):
        graph[p].append(i)

    tree = LinkCutTree([[] for _ in range(N)], [0] * N, lambda x, y: x + y)
    assert list(tree.left) == [-1] * N
    assert list(tree.right) == [-1] * N
    assert list(tree.parent) == [-1] * N

    graph = [[1, 2], [], [3, 4], [], []]

    tree.link(0, 1)
    assert list(tree.left) == [-1, -1, -1, -1, -1]
    assert list(tree.right) == [1, -1, -1, -1, -1]
    assert list(tree.parent) == [-1, 0, -1, -1, -1]

    tree.link(0, 2)
    assert list(tree.left) == [-1, -1, -1, -1, -1]
    assert list(tree.right) == [2, -1, -1, -1, -1]
    assert list(tree.parent) == [-1, 0, 0, -1, -1]

    tree.link(2, 3)
    assert list(tree.left) == [-1, -1, 0, -1, -1]
    assert list(tree.right) == [-1, -1, 3, -1, -1]
    assert list(tree.parent) == [2, 0, -1, 2, -1]

    tree.link(2, 4)
    assert list(tree.left) == [-1, -1, 0, -1, -1]
    assert list(tree.right) == [-1, -1, 4, -1, -1]
    assert list(tree.parent) == [2, 0, -1, 2, 2]


def test_expose():
    N = 5
    P = [0, 0, 2, 2]

    graph = [[] for _ in range(N)]
    for i, p in enumerate(P, start=1):
        graph[p].append(i)

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)

    tree.expose(0)
    assert list(tree.left) == [-1, -1, -1, -1, -1]
    assert list(tree.right) == [-1, -1, 4, -1, -1]
    assert list(tree.parent) == [-1, 0, 0, 2, 2]

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)
    tree.expose(1)
    assert list(tree.left) == [-1, 0, -1, -1, -1]
    assert list(tree.right) == [-1, -1, 4, -1, -1]
    assert list(tree.parent) == [1, -1, 0, 2, 2]

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)
    tree.expose(2)
    assert list(tree.left) == [-1, -1, 0, -1, -1]
    assert list(tree.right) == [-1, -1, -1, -1, -1]
    assert list(tree.parent) == [2, 0, -1, 2, 2]

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)
    tree.expose(3)
    assert list(tree.left) == [-1, -1, 0, 2, -1]
    assert list(tree.right) == [-1, -1, -1, -1, -1]
    assert list(tree.parent) == [2, 0, 3, -1, 2]

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)
    tree.expose(4)
    assert list(tree.left) == [-1, -1, 0, -1, 2]
    assert list(tree.right) == [-1, -1, -1, -1, -1]
    assert list(tree.parent) == [2, 0, 4, 2, -1]


def test_lca():
    N = 5
    P = [0, 0, 2, 2]

    graph = [[] for _ in range(N)]
    for i, p in enumerate(P, start=1):
        graph[p].append(i)

    tree = LinkCutTree(graph, [0] * N, lambda x, y: x + y)
    assert tree.lowest_common_ancestor(0, 1) == 0
    assert tree.lowest_common_ancestor(0, 4) == 0
    assert tree.lowest_common_ancestor(1, 2) == 0
    assert tree.lowest_common_ancestor(2, 3) == 2
    assert tree.lowest_common_ancestor(3, 4) == 2


def test_evert():
    N = 5
    value = [1, 10, 100, 1000, 10000]
    edges = [(0, 1), (1, 2), (2, 3), (1, 4)]

    graph = [[] for _ in range(N)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    tree = LinkCutTree[int](
        graph,
        value,
        lambda x, y: x + y,
    )

    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.add(1, 100000)
    value[1] += 100000
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.evert(0)
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.evert(1)
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.evert(2)
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.evert(3)
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]

    tree.evert(4)
    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[1] + value[2]
    assert tree.query(0, 3) == value[0] + value[1] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[2]
    assert tree.query(1, 3) == value[1] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[1] + value[0]
    assert tree.query(2, 1) == value[2] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[1] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]


def test_split_merge_query():
    N = 5
    value = [1, 10, 100, 1000, 10000]
    edges = [(0, 1), (1, 2), (2, 3), (1, 4)]

    graph = [[] for _ in range(N)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    tree = LinkCutTree[int](
        graph,
        value,
        lambda x, y: x + y,
    )
    tree.add(1, 100000)
    value[1] += 100000

    # u, v = 1, 2
    # tree.evert(u)
    tree.split(1, 2)
    tree.merge(2, 0)

    assert tree.query(0, 0) == value[0]
    assert tree.query(0, 1) == value[0] + value[1]
    assert tree.query(0, 2) == value[0] + value[2]
    assert tree.query(0, 3) == value[0] + value[2] + value[3]
    assert tree.query(0, 4) == value[0] + value[1] + value[4]

    assert tree.query(1, 0) == value[0] + value[1]
    assert tree.query(1, 1) == value[1]
    assert tree.query(1, 2) == value[1] + value[0] + value[2]
    assert tree.query(1, 3) == value[1] + value[0] + value[2] + value[3]
    assert tree.query(1, 4) == value[1] + value[4]

    assert tree.query(2, 0) == value[2] + value[0]
    assert tree.query(2, 1) == value[2] + value[0] + value[1]
    assert tree.query(2, 2) == value[2]
    assert tree.query(2, 3) == value[2] + value[3]
    assert tree.query(2, 4) == value[2] + value[0] + value[1] + value[4]

    assert tree.query(3, 0) == value[3] + value[2] + value[0]
    assert tree.query(3, 1) == value[3] + value[2] + value[0] + value[1]
    assert tree.query(3, 2) == value[3] + value[2]
    assert tree.query(3, 3) == value[3]
    assert tree.query(3, 4) == value[3] + value[2] + value[0] + value[1] + value[4]

    assert tree.query(4, 0) == value[4] + value[1] + value[0]
    assert tree.query(4, 1) == value[4] + value[1]
    assert tree.query(4, 2) == value[4] + value[1] + value[0] + value[2]
    assert tree.query(4, 3) == value[4] + value[1] + value[0] + value[2] + value[3]
    assert tree.query(4, 4) == value[4]
