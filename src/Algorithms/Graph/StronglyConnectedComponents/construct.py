from src.common.Graph.type import AdjacencyList


def construct(graph: AdjacencyList, scc: list[list[int]]) -> AdjacencyList:
    """強連結成分から強連結成分グラフを構築する

    Args:
        graph (AdjacencyList): 元の有向グラフ
        scc (list[list[int]]): 強連結成分. [[v1, v2, v3, ...], [v4, v5, ...], ...]

    Returns:
        AdjacencyList: 強連結成分グラフ (縮約後のグラフ)
    """
    N = len(graph)

    # labels[v]: 頂点vの縮約後の頂点番号
    labels = [-1] * N
    for i, component in enumerate(scc):
        for v in component:
            labels[v] = i

    scc_graph = [set() for _ in range(len(scc))]
    for u in range(N):
        for v in graph[u]:
            if labels[u] == labels[v]:
                continue

            scc_graph[labels[u]].add(labels[v])

    return [list(s) for s in scc_graph]
