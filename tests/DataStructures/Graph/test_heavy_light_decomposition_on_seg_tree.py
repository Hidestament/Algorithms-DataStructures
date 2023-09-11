from src.DataStructures.Graph.heavy_light_decomposition_on_seg_tree import HeavyLightDecompositionOnSegmentTree


def test_library_checker_case1():
    N = 5
    value = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    edges = [(0, 1), (1, 2), (2, 3), (2, 4)]

    graph = [[] for _ in range(N)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    MOD = 998244353
    hl = HeavyLightDecompositionOnSegmentTree[tuple[int, int]](
        graph,
        value,
        segfunc=lambda x, y: ((y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD),
        ide_ele=(1, 0),
    )
    u, v, x = 0, 3, 11
    func = hl.vertex_aggregation_value(u, v)
    assert func[0] * x + func[1] == 1555

    u, v, x = 2, 4, 12
    func = hl.vertex_aggregation_value(u, v)
    assert func[0] * x + func[1] == 604

    p, c, d = 2, 13, 14
    hl.update_vertex_value(p, (c, d))

    u, v, x = 0, 4, 15
    func = hl.vertex_aggregation_value(u, v)
    assert func[0] * x + func[1] == 6571

    u, v, x = 2, 2, 16
    func = hl.vertex_aggregation_value(u, v)
    assert func[0] * x + func[1] == 222


def test_library_checker_case2():
    N = 7
    value = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
    ]
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6)]

    graph = [[] for _ in range(N)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    MOD = 998244353
    hl = HeavyLightDecompositionOnSegmentTree[tuple[int, int]](
        graph,
        value,
        segfunc=lambda x, y: ((y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD),
        ide_ele=(1, 0),
    )

    u, v, x = 2, 4, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 411

    u, v, x = 4, 6, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 2199

    u, v, x = 6, 2, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 607

    p, c, d = 1, 20, 30
    hl.update_vertex_value(p, (c, d))

    u, v, x = 2, 4, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 3471

    u, v, x = 4, 6, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 2199

    u, v, x = 6, 2, 1
    func = hl.vertex_aggregation_value(u, v)
    assert (func[0] * x + func[1]) % MOD == 6034
