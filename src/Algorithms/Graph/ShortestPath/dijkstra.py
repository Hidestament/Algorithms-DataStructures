from heapq import heappush, heappop

from src.common.Graph.type import AdjacencyListWithWeight


def dijkstra(graph: AdjacencyListWithWeight, start: int) -> tuple[list[int], list[int]]:
    """単一始点最短経路 (SSSP) を求める. 経路復元のための先行頂点も求める.

    Args:
        graph (AdjacencyListWithWeight): 重み付きグラフ. 辺の重みは非負であること.
        start (int): 始点.

    Returns:
        tuple[list[int], list[int]]: (距離, 先行頂点). 到達できない場合は float("INF"), -1 が入る.

    TimeComplexity:
        O((E + V) log V)
    """
    dist = [float("INF")] * len(graph)
    # 先行頂点
    prev = [-1] * len(graph)
    # 確定したかどうか
    flag = [False] * len(graph)

    # (距離, 頂点番号, 先行頂点)
    hq = [(0, start, -1)]
    while hq:
        cost, now_v, prev_v = heappop(hq)

        # 確定した頂点はスキップ
        if flag[now_v]:
            continue
        flag[now_v] = True
        dist[now_v] = cost
        prev[now_v] = prev_v

        for to_v, weight in graph[now_v]:
            if flag[to_v]:
                continue

            # 最短経路が更新された場合
            if dist[now_v] + weight < dist[to_v]:
                heappush(hq, (dist[now_v] + weight, to_v, now_v))

    return dist, prev
