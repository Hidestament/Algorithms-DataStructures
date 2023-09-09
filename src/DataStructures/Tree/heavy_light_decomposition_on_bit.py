from typing import Optional
from collections import deque
from itertools import chain

from src.common.Graph.type import AdjacencyList
from src.DataStructures.RangeTree.binary_indexed_tree import BinaryIndexedTree


class HeavyLightDecompositionOnBIT:
    """HL分解 (非再帰)

    Attributes:
        prev (list[int]): vの先行頂点
        depth_on_heavy_path (list[int]): 頂点vが属するheavy path上でのheadからの距離
        heavy_node (list[list[int]]): 縮約後の頂点列
        heavy_node_depth (list[int]): 縮約御の頂点の深さ
        heavy_node_mappings (list[int]): 頂点vが属する集約後の頂点番号
        heavy_node_start_on_bit (list[int]): bit上でのheavy_nodeの開始位置
        bit (BinaryIndexedTree): 頂点の重みを管理するBIT

    Methods:
        lowest_common_ancestor(u, v): u, vの最小共通祖先を求める, O(log N)
        get_vertex_weight(u): 頂点uの重みを返す, O(log N)
        add_vertex_weight(u, w): 頂点uの重みにwを加算する (V_u += w), O(log N)
        add_vertex_weight(u, w): 頂点uの重みをwに変更する (V_u = w), O(log N)
        vertex_sum_from_root(u): root -> u の頂点の重みの和を求める (root, uの重みも含む), O((log N)^2)
        vertex_sum(u, v): u -> v の頂点の重みの和を求める (u, vの重みも含む), O((log N)^2)
    """

    def __init__(
        self,
        graph: AdjacencyList,
        weights: list[int],
        root: int = 0,
    ):
        """HL分解

        Args:
            graph (AdjacencyList): 木グラフ
            weights (list[int]): 頂点の重み
            root (int): 根とする頂点

        TimeComplexity:
            O(N logN)
        """
        N = len(graph)

        # prev[v]: vの先行頂点
        self.prev = [-1] * N
        # depth_on_heavy_path[v]: 頂点vが属するheavy path上でのheadからの距離
        self.depth_on_heavy_path = [0] * N
        # 縮約後の頂点列
        self.heavy_node = []
        # 縮約御の頂点の深さ
        self.heavy_node_depth = []
        # heavy_node_mappings[v]: 頂点vが属する集約後の頂点番号
        self.heavy_node_mappings = [-1] * N
        # heavy_node_start_on_bit[v]: bit上でのheavy_nodeの開始位置
        self.heavy_node_start_on_bit = []

        self._build(graph, weights, root)

    def _calculate_heavy_child(
        self,
        graph: AdjacencyList,
        root: int,
    ) -> list[Optional[int]]:
        """全ての頂点のheavy childを計算する

        Args:
            graph (AdjacencyList): 木グラフ
            root (int): 根とする頂点

        Returns:
            list[Optional[int]]: heavy_child[v] -> vのheavyな子頂点

        Notes:
            以下も計算する
            prev: vの先行頂点

        TimeComplexity:
            O(N)
        """
        N = len(graph)
        status = [False] * N
        subtree_size = [1] * N
        heavy_child = [None] * N

        dq = deque([(root, -1)])
        while dq:
            now, parent = dq[-1]

            if status[now]:
                self.prev[now] = parent

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
                dq.append((to, now))

        return heavy_child

    def _decompose(
        self,
        graph: AdjacencyList,
        root: int,
        heavy_child: list[Optional[int]],
    ):
        """HL分解

        Args:
            graph (AdjacencyList): 木グラフ
            root (int): 根
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

    def _build_bit(self, weights: list[int]):
        """BITの構築

        Args:
            weights (list[int]): 頂点の重み

        TimeComplexity:
            O(N logN)
        """
        bit = [weights[v] for v in chain.from_iterable(self.heavy_node)]
        self.bit = BinaryIndexedTree(bit)

        s = 0
        for heavy in self.heavy_node:
            self.heavy_node_start_on_bit.append(s)
            s += len(heavy)

    def _build(
        self,
        graph: AdjacencyList,
        weights: list[int],
        root: int,
    ):
        """HL分解 & BITの構築 を行う

        Args:
            graph (AdjacencyList): 木グラフ
            weights (list[int]): 頂点の重み
            root (int): 根とする頂点

        TimeComplexity:
            O(N logN)
        """
        heavy_child = self._calculate_heavy_child(graph, root)
        self._decompose(graph, root, heavy_child)
        self._build_bit(weights)

    def _get_heavy_node_depth(self, u: int) -> int:
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

    def _get_bit_index(self, u: int) -> int:
        """BIT上での頂点uのindexを返す

        Args:
            u (int): 頂点 (縮約前)

        Returns:
            int: BIT上でのindex
        """
        heavy_node = self.heavy_node_mappings[u]
        head_ind = self.heavy_node_start_on_bit[heavy_node]
        ind = head_ind + self.depth_on_heavy_path[u]
        return ind

    def get_vertex_weight(self, u: int) -> int:
        """頂点uの重みを返す

        Args:
            u (int): 頂点 (縮約前)

        Returns:
            int: 頂点uの重み
        """
        return self.bit.get(self._get_bit_index(u))

    def add_vertex_weight(self, u: int, w: int):
        """頂点uの重みにwを加算する (V_u += w)

        Args:
            u (int): 頂点 (縮約前)
            w (int): 加算値
        """
        self.bit.add(self._get_bit_index(u), w)

    def update_vertex_weight(self, u: int, w: int):
        """頂点uの重みをwに変更する (V_u = w)

        Args:
            u (int): 頂点 (縮約前)
            w (int): 変更値
        """
        self.bit.update(self._get_bit_index(u), w)

    def vertex_sum_from_root(self, u: int) -> int:
        """root -> u の頂点の重みの和を求める (root, uの重みも含む)

        Args:
            u (int): 頂点 (縮約前)

        Returns:
            int: root -> u の頂点の重みの和

        TimeComplexity:
            O((log N)^2)
        """
        s = 0

        # uのheavy pathのheadからuまでの頂点の重みの和
        heavy_u = self.heavy_node_mappings[u]
        head_ind = self.heavy_node_start_on_bit[heavy_u]
        heavy_u_ind = head_ind + self.depth_on_heavy_path[u] + 1
        s += self.bit.sum_range(head_ind, heavy_u_ind)

        while heavy_u != 0:
            u = self.prev[self.heavy_node[heavy_u][0]]
            heavy_u = self.heavy_node_mappings[u]
            head_ind = self.heavy_node_start_on_bit[heavy_u]
            heavy_u_ind = head_ind + self.depth_on_heavy_path[u] + 1
            s += self.bit.sum_range(head_ind, heavy_u_ind)

        return s

    def vertex_sum(self, u: int, v: int) -> int:
        """u -> v の頂点の重みの和を求める (u, vの重みも含む)

        Args:
            u (int): 頂点 (縮約前)
            v (int): 頂点 (縮約前)

        Returns:
            int: u -> v の頂点の重みの和

        TimeComplexity:
            O((log N)^2)
        """
        lca = self.lowest_common_ancestor(u, v)

        dist_u = self.vertex_sum_from_root(u)
        dist_v = self.vertex_sum_from_root(v)
        dist_lca = self.vertex_sum_from_root(lca)

        s = dist_u + dist_v - 2 * dist_lca + self.get_vertex_weight(lca)
        return s
