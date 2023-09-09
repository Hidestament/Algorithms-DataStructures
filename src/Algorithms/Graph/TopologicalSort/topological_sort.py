from heapq import heapify, heappop, heappush

from src.common.Graph.type import AdjacencyList


def topological_sort(graph: AdjacencyList, indegree: list[int]) -> list[int]:
    """辞書順最小にトポロジカルソートする (非再帰)

    Args:
        graph (AdjacencyList): 有向グラフ
        indegree (list[int]): 各頂点の入次数

    Returns:
        list[int]: トポロジカルソートされた頂点番号 (辞書順最小)

    TimeComplexity:
        O((V+E)logV)
    """
    N = len(graph)

    # 隣接リストの頂点の順序をソートする
    for v in graph:
        v.sort()

    vertex_order = []
    hq = [v for v in range(N) if indegree[v] == 0]
    heapify(hq)

    while hq:
        now = heappop(hq)
        vertex_order.append(now)

        for to in graph[now]:
            indegree[to] -= 1
            if indegree[to] == 0:
                heappush(hq, to)

    return vertex_order
