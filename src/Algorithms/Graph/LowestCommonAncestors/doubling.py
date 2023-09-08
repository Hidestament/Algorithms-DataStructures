from __future__ import annotations

from typing import Union
from collections import deque


class LowestCommonAncestorsDoubling:
    """Doublingを用いたLCAを計算するクラス.
    0. 初期化 (O(N log N))
    1. calculate_lca(u, v): uとvのLCAを計算する (O(log N))
    2. calculate_distance(u, v): uとvの距離を計算する (O(log N))
    """

    def __init__(self, graph: list, root: int = 0, weighted: bool = False):
        """コンストラクタ. 以下を計算する.
            1. 根から各頂点への距離.
            2. 各頂点への深さ.
            3. 2^k回親を辿った頂点 (ダブリング).

        Args:
            graph (list): グラフの隣接リスト. 木である必要がある.
            root (int): 根. Defaults to 0.
            weighted (bool): 重み付きグラフかどうか. Defaults to False.

        Examples:
            重み付きの場合
                graph[v]: [(u, w), ...], (v -> u)の辺と重みw
            重み無しの場合
                graph[v]: [u, ...], (v -> u)の辺
        """
        self._graph = graph
        self._root = root

        # 重み無しの場合, 重みを全て1としたグラフを構成する
        if not weighted:
            for v in range(len(graph)):
                self._graph[v] = [(u, 1) for u in graph[v]]

        # ダブリングに必要なものの計算
        self.distance = [-1] * len(self._graph)
        self.depth = [-1] * len(self._graph)
        self.prev_ancestor = [-1] * len(self._graph)
        self._init_bfs()

        # ダブリングの配列の構築
        self.doubling = self._init_doubling()

    def _init_bfs(self) -> None:
        """bfsによる初期化. 以下を計算する.
        1. 根から各頂点への距離.
        2. 各頂点への深さ.
        3. 各頂点の親.
        """
        dq = deque()
        dq.append((self._root, -1, 0, 0))

        while dq:
            now, prev, dist, depth = dq.popleft()
            self.prev_ancestor[now] = prev
            self.distance[now] = dist
            self.depth[now] = depth

            for to, weight in self._graph[now]:
                if to == prev:
                    continue
                dq.append((to, now, dist + weight, depth + 1))

    def _init_doubling(self) -> list[list[int]]:
        """ダブリングの初期化.
        vの2^k先の親 = vの2^(k-1)の2^(k-1)の先の親 より計算する

        Returns:
            list[list[int]]: doubling[k][i]: iの2^k先の親
        """
        max_depth = max(self.depth)
        max_k = (max_depth - 1).bit_length()

        # doubling[k][i]: iの2^k先の親
        doubling = [[-1] * len(self._graph) for _ in range(max_k + 1)]
        doubling[0] = self.prev_ancestor

        for k in range(1, max_k + 1):
            for v in range(len(self._graph)):
                if doubling[k - 1][v] == -1:
                    doubling[k][v] = -1
                else:
                    doubling[k][v] = doubling[k - 1][doubling[k - 1][v]]

        return doubling

    def _calculate_ancestors(self, u: int, k: int) -> int:
        """uのk個先の親を計算する

        Args:
            u (int): 対象の頂点
            k (int): k個先の親

        Returns:
            int: uのk個先の親
        """
        parent = u
        bit = 0
        while k:
            if k % 2:
                parent = self.doubling[bit][parent]

            k >>= 1
            bit += 1

        return parent

    def calculate_lca(self, u: int, v: int) -> int:
        """uとvのLCAを計算する

        Args:
            u (int): 頂点u
            v (int): 頂点v

        Returns:
            int: uとvのlca
        """
        u_depth, v_depth = self.depth[u], self.depth[v]

        # uの深さ > vの深さにする
        if u_depth < v_depth:
            u, v = v, u
            u_depth, v_depth = v_depth, u_depth

        # 高さを揃える
        diff_depth = u_depth - v_depth
        u = self._calculate_ancestors(u, diff_depth)

        if u == v:
            return u

        # 2^kずつ親を確認する
        max_k = (v_depth - 1).bit_length()
        for k in range(max_k, -1, -1):
            u_next = self.doubling[k][u]
            v_next = self.doubling[k][v]

            if u_next != v_next:
                u, v = u_next, v_next

        lca = self.doubling[0][u]
        return lca

    def calculate_distance(self, u: int, v: int) -> Union[int, float]:
        """u, vの距離を計算する

        Args:
            u (int): 頂点u
            v (int): 頂点v

        Returns:
            Union[int, float]: dist(u, v)
        """
        lca = self.calculate_lca(u, v)
        return self.distance[u] + self.distance[v] - 2 * self.distance[lca]


if __name__ == "__main__":
    N = int(input())
    graph = [[] for _ in range(N)]
    for now in range(N):
        child = list(map(int, input().split()))
        if child[0] == 0:
            continue
        for to in child[1:]:
            graph[now].append(to)

    lca = LowestCommonAncestorsDoubling(graph, root=0)

    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        print(lca.calculate_lca(u, v))
