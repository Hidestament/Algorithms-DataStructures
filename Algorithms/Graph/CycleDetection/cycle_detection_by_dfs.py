from typing import Deque
from collections import deque

from Algorithms.Graph.Common.type import AdjacencyListWithEdgeNumber


def _dfs_no_recursion(
    graph: AdjacencyListWithEdgeNumber,
    status: list[int],
    root: int,
) -> (Deque[tuple[int, int]], int):
    """非再帰DFS. 閉路が存在する場合は閉路の頂点列を返す.

    Args:
        graph (AdjacencyListWithEdgeNumber): グラフの隣接リスト. 辺の番号も持つ. 連結・単純・無向どちらでもOK.
        status: list[int]: 頂点の状態: -1 -> 未訪問, 0 -> 探索中, 1 -> 探索終了.
        root (int): 探索の起点となる頂点.

    Returns:
        (Deque[tuple[int, int]], int): 探索中の(頂点, 辺)列, 閉路の起点. 閉路が存在しない場合は-1.
    """
    # 探索対象の頂点 (頂点, 辿ってきた辺)
    dq = deque([(root, -1)])
    # 探索中の頂点
    searching = deque([])
    while dq:
        now_v, now_e = dq[-1]

        # 全ての子頂点の探索が終了した頂点
        if status[now_v] == 0:
            status[now_v] = 1
            dq.pop()
            searching.pop()
            continue

        status[now_v] = 0
        searching.append((now_v, now_e))

        for to_v, to_e in graph[now_v]:
            # 親頂点の場合はスキップ
            if to_e == now_e:
                continue

            # すでに探索済みの頂点はスキップ
            if status[to_v] == 1:
                continue

            # 探索中の頂点にいける -> 閉路が存在する
            if status[to_v] == 0:
                searching.append((to_v, to_e))
                return searching, to_v

            dq.append((to_v, to_e))

    return searching, -1


def _restore_cycle(
    searching: Deque[tuple[int, int]], start: int
) -> (list[int], list[int]):
    """閉路の頂点列を復元する.

    Args:
        searching (Deque[tuple[int, int]]): DFSで得た探索中の(頂点, 辺)列.
        start (int): 閉路の起点.

    Returns:
        (list[int], list[int]): 閉路の頂点列, 閉路の辺列.
    """
    while searching[0][0] != start:
        searching.popleft()
    searching.popleft()

    cycle_v = list([v for v, _ in searching])
    cycle_e = list([e for _, e in searching]) + [searching[0][1]]
    return cycle_v, cycle_e[1:]


def cycle_detection(graph: AdjacencyListWithEdgeNumber) -> (list[int], list[int]):
    """グラフにおける閉路の検出. 非再帰DFSを使用. 閉路が存在するならば閉路の頂点列, 辺列を1つ返す.

    Args:
        graph (AdjacencyListWithEdgeNumber): グラフの隣接リスト. 辺の番号も持つ. 連結・単純・無向どちらでもOK.

    Returns:
        (list[int], list[int]): (閉路の頂点列, 閉路の辺列). 存在しない場合は空リスト.

    TimeComplexity:
        O(N + M)
    """
    N = len(graph)

    # 頂点の状態: -1 -> 未訪問, 0 -> 探索中, 1 -> 探索終了
    status = [-1] * N
    for root in range(N):
        if status[root] != -1:
            continue

        path, start = _dfs_no_recursion(graph, status, root)

        # 閉路が存在する場合
        if start != -1:
            cycle_v, cycle_e = _restore_cycle(path, start)
            return cycle_v, cycle_e

    return [], []
