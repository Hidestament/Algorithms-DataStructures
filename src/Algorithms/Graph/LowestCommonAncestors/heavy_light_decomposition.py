from typing import Optional, Union
from collections import deque

from src.common.Graph.type import AdjacencyList, AdjacencyListWithWeight


class HeavyLightDecomposition:
    """LCAを求めるためのHL分解 (非再帰)

    Attributes:
        prev (list[int]): vの先行頂点
        _dist (list[int]): vの根からの距離
        depth_on_heavy_path (list[int]): 頂点vが属するheavy path上でのheadからの距離
        heavy_node (list[list[int]]): 縮約後の頂点列
        heavy_node_depth (list[int]): 縮約御の頂点の深さ
        self.heavy_node_mappings (list[int]): 頂点vが属する集約後の頂点番号

    Methods:
        lowest_common_ancestor(u, v): u, vの最小共通祖先を求める, O(log N)
        dist_from_root(u): 頂点uの根からの距離を求める, O(1)
        dist(u, v): 頂点u, vの距離を求める, O(log N)
    """

    def __init__(
        self,
        graph: Union[AdjacencyList, AdjacencyListWithWeight],
        root: int = 0,
        weighted: bool = False
    ):
        """HL分解

        Args:
            graph (Union[AdjacencyList, AdjacencyListWithWeight]): 木グラフ. weighted=Trueの場合は, AdjacencyListWithWeight
            root (int): 根とする頂点
            weighted (bool): True -> 重み付き, False -> 重みなし.

        TimeComplexity:
            O(N)
        """
        N = len(graph)

        # prev[v]: vの先行頂点
        self.prev = [-1] * N
        # dist[v]: vの根からの距離
        self._dist = [0] * N
        # depth_on_heavy_path[v]: 頂点vが属するheavy path上でのheadからの距離
        self.depth_on_heavy_path = [0] * N
        # 縮約後の頂点列
        self.heavy_node = []
        # 縮約御の頂点の深さ
        self.heavy_node_depth = []
        # heavy_node_mappings[v]: 頂点vが属する集約後の頂点番号
        self.heavy_node_mappings = [-1] * N

        self._build(graph, root, weighted)

    def _calculate_heavy_child_no_weight(
        self,
        graph: Union[AdjacencyList, AdjacencyListWithWeight],
        root: int,
    ) -> list[Optional[int]]:
        """全ての頂点のheavy childを計算する (重み無しグラフ)

        Args:
            graph (Union[AdjacencyList, AdjacencyListWithWeight]): 木グラフ.
            root (int): 根とする頂点

        Returns:
            list[Optional[int]]: heavy_child[v] -> vのheavyな子頂点

        Notes:
            以下も計算する
            prev: vの先行頂点
            _dist: vの深さ

        TimeComplexity:
            O(N)
        """
        N = len(graph)
        status = [False] * N
        subtree_size = [1] * N
        heavy_child = [None] * N

        dq = deque([(root, -1, 0)])
        while dq:
            now, parent, d = dq[-1]

            if status[now]:
                self.prev[now] = parent
                self._dist[now] = d

                max_subtree = 0
                for to in graph[now]:
                    if to == parent:
                        continue
                    subtree_size[now] += subtree_size[to]
                    if subtree_size[to] > max_subtree:
                        heavy_child[now] = to
                        max_subtree = subtree_size[to]

                dq.pop()

            status[now] = True
            for to in graph[now]:
                if status[to]:
                    continue
                dq.append((to, now, d + 1))

        return heavy_child

    def _calculate_heavy_child_with_weight(
        self,
        graph: Union[AdjacencyList, AdjacencyListWithWeight],
        root: int,
    ) -> list[Optional[int]]:
        """全ての頂点のheavy childを計算する (重み付きグラフ)

        Args:
            graph (Union[AdjacencyList, AdjacencyListWithWeight]): 木グラフ.
            root (int): 根とする頂点

        Returns:
            list[Optional[int]]: heavy_child[v] -> vのheavyな子頂点

        Notes:
            以下も計算する
            prev: vの先行頂点
            _dist: vの根からの距離

        TimeComplexity:
            O(N)
        """
        N = len(graph)
        status = [False] * N
        subtree_size = [1] * N
        heavy_child = [None] * N

        dq = deque([(root, -1, 0)])
        while dq:
            now, parent, d = dq[-1]

            if status[now]:
                self.prev[now] = parent
                self._dist[now] = d

                max_subtree = 0
                for to, _ in graph[now]:
                    if to == parent:
                        continue
                    subtree_size[now] += subtree_size[to]
                    if subtree_size[to] > max_subtree:
                        heavy_child[now] = to
                        max_subtree = subtree_size[to]

                dq.pop()

            status[now] = True
            for to, w in graph[now]:
                if status[to]:
                    continue
                dq.append((to, now, d + w))

        return heavy_child

    def _decomposition(
        self,
        graph: Union[AdjacencyList, AdjacencyListWithWeight],
        root: int,
        heavy_child: list[Optional[int]]
    ):
        """heavy_childをもとに, heavy pathを縮約しHL分解する

        Args:
            graph (Union[AdjacencyList, AdjacencyListWithWeight]): 木グラフ.
            root (int): 根とする頂点
            heavy_child (list[Optional[int]]): 各頂点のheavyな子頂点

        Notes:
            以下も計算する
            depth_on_heavy_path[v]: 頂点vが属するheavy path上でのheadからの距離
            heavy_node_mappings[v]: 頂点vが属する集約後の頂点番号
            heavy_node: 集約後の頂点列
            heavy_node_depth: 集約後の頂点の深さ

        TimeComplexity:
            O(N)
        """
        # (root, d): heavy_pathの根(始点), 深さ
        dq = deque([(root, 0)])
        while dq:
            # 最初に, vからheavy pathをたどる
            root, depth = dq.popleft()
            heavy_path = []

            now = root
            while now is not None:
                # nowに繋がるlightな頂点をdequeに入れる
                for to in graph[now]:
                    # 辿ってきたpath or heavyな頂点ならスキップ
                    if (to == self.prev[now]) or (to == heavy_child[now]):
                        continue
                    dq.append((to, depth + 1))

                self.heavy_node_mappings[now] = len(self.heavy_node)
                self.depth_on_heavy_path[now] = len(heavy_path)
                heavy_path.append(now)

                now = heavy_child[now]

            self.heavy_node.append(heavy_path)
            self.heavy_node_depth.append(depth)

    def _build(
        self,
        graph: Union[AdjacencyList, AdjacencyListWithWeight],
        root: int,
        weighted: bool,
    ):
        """HL分解を行う

        Args:
            graph (Union[AdjacencyList, AdjacencyListWithWeight]): 木グラフ
            root (int): 根とする頂点
            weighted (bool): True -> 重み付き, False -> 重みなし.
        """
        heavy_child = self._calculate_heavy_child_with_weight(graph, root) \
            if weighted else self._calculate_heavy_child_no_weight(graph, root)
        self._decomposition(graph, root, heavy_child)

    def _head(self, v):
        # 頂点vが属するheavy pathの先頭 (最も根に近い頂点)
        heavy_node = self.heavy_node_mappings[v]
        return self.heavy_node[heavy_node][0]

    def _get_heavy_node_depth(self, u) -> int:
        """uが属するheavy nodeの深さを返す

        Args:
            u (int): 元のグラフの頂点

        Returns:
            int: uが属する縮約後の頂点の深さ
        """
        return self.heavy_node_depth[self.heavy_node_mappings[u]]

    def lowest_common_ancestor(self, u: int, v: int) -> int:
        """u, vの最小共通祖先を求める

        Args:
            u (int): 頂点
            v (int): 頂点

        Returns:
            int: u, vの最小共通祖先

        TimeComplexity:
            O(log N)
        """
        # vを深い方の頂点に統一する
        if self._get_heavy_node_depth(u) > self._get_heavy_node_depth(v):
            u, v = v, u

        depth_diff = self._get_heavy_node_depth(v) - self._get_heavy_node_depth(u)
        heavy_u = self.heavy_node_mappings[u]
        heavy_v = self.heavy_node_mappings[v]

        # vをuと同じ深さまで遡る
        for _ in range(depth_diff):
            # heavy_vの親頂点のtail node
            v = self.prev[self.heavy_node[heavy_v][0]]
            heavy_v = self.heavy_node_mappings[v]

        # u, vが同じ頂点になるまで遡る
        while heavy_u != heavy_v:
            u = self.prev[self.heavy_node[heavy_u][0]]
            heavy_u = self.heavy_node_mappings[u]
            v = self.prev[self.heavy_node[heavy_v][0]]
            heavy_v = self.heavy_node_mappings[v]

        # u, vが同じheavy pathにいるので, 根に近い方がLCA
        return u if self.depth_on_heavy_path[u] < self.depth_on_heavy_path[v] else v

    def dist_from_root(self, u: int) -> int:
        """頂点uの根からの距離を求める

        Args:
            u (int): 頂点

        Returns:
            int: 頂点uの根からの距離

        TimeComplexity:
            O(1)
        """
        return self._dist[u]

    def dist(self, u: int, v: int) -> int:
        """頂点u, vの距離を求める

        Args:
            u (int): 頂点
            v (int): 頂点

        TimeComplexity:
            O(log N)
        """
        lca = self.lowest_common_ancestor(u, v)
        return self.dist(u) + self.dist(v) - 2 * self.dist(lca)
