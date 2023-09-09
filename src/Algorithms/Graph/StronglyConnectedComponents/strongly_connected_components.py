from collections import deque

from src.common.Graph.type import AdjacencyList


def _dfs1(
    graph: AdjacencyList,
    root: int,
    seen: list[int],
    post_ordering: list[int],
) -> list[int]:
    """帰りがけで頂点を記録するDFS (非再帰)

    Args:
        graph (AdjacencyList): 有向グラフ
        root (int): 探索開始頂点
        seen (list[int]): 頂点の探索状況. -1 -> 未訪問, 0 -> 探索中, 1 -> 探索済
        post_ordering (list[int]): 帰りがけ順の頂点番号

    Returns:
        list[int]: 帰りがけ順の頂点番号
    """
    dq = deque([root])
    while dq:
        now = dq[-1]

        if seen[now] == 1:
            dq.pop()
            continue

        # 探索中の頂点に戻ってきたら終了
        if seen[now] == 0:
            seen[now] = 1
            post_ordering.append(now)
            dq.pop()
            continue

        seen[now] = 0
        for to in graph[now]:
            if seen[to] != -1:
                continue
            dq.append(to)

    return post_ordering


def dfs2(
    reverse_graph: AdjacencyList,
    root: int,
    seen: list[int],
) -> list[int]:
    """逆辺に沿って頂点を記録するDFS (非再帰)

    Args:
        reverse_graph (AdjacencyList): 有向グラフの逆辺
        root (int): 探索開始頂点
        seen (list[int]): 頂点の探索状況. 0 -> 未訪問, 1 -> 探索済

    Returns:
        list[int]: 強連結成分
    """
    dq = deque([root])
    components = []
    while dq:
        now = dq.pop()
        if seen[now]:
            continue

        components.append(now)
        seen[now] = 1
        for to in reverse_graph[now]:
            if seen[to]:
                continue
            dq.append(to)

    return components


def strongly_connected_components(
    graph: AdjacencyList,
    reverse_graph: AdjacencyList,
) -> list[list[int]]:
    """強連結成分分解

    Args:
        graph (AdjacencyList): 有向グラフ
        reverse_graph (AdjacencyList): 有向グラフの逆辺

    Returns:
        list[list[int]]: 強連結成分. [[v1, v2, v3], [v4, v5], ...]の形式

    TimeComplexity:
        O(V + E)
    """
    N = len(graph)

    # 1回目DFS: 帰りがけで頂点を記録
    seen = [-1] * N
    post_ordering = []
    for root in range(N):
        if seen[root] == 1:
            continue
        _dfs1(graph, root, seen, post_ordering)

    # 2回目DFS: 逆辺に沿って頂点を記録
    seen = [0] * N
    strongly_connected_components = []
    for root in reversed(post_ordering):
        if seen[root] == 1:
            continue
        components = dfs2(reverse_graph, root, seen)
        strongly_connected_components.append(components)

    return strongly_connected_components
