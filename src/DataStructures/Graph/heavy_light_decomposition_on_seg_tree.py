from typing import Optional, Callable, TypeVar, Generic
from collections import deque
from itertools import chain

from src.common.Graph.type import AdjacencyList
from src.DataStructures.RangeTree.segment_tree import SegmentTree


T = TypeVar("T")


class HeavyLightDecompositionOnSegmentTree(Generic[T]):
    """HL分解 + SegmentTree(非再帰)

    Attributes:
        prev (list[int]): vの先行頂点
        depth_on_heavy_path (list[int]): 頂点vが属するheavy path上でのheadからの距離
        heavy_node (list[list[int]]): 縮約後の頂点列
        heavy_node_depth (list[int]): 縮約御の頂点の深さ
        heavy_node_mappings (list[int]): 頂点vが属する集約後の頂点番号
        heavy_node_start_on_seg_tree (list[int]): bit上でのheavy_nodeの開始位置
        seg_tree1 (SegmentTree[T]): root -> u 方向の頂点の集約値を管理するSegmentTree
        seg_tree2 (SegmentTree[T]): u -> root 方向の頂点の集約値を管理するSegmentTree (演算が可換の場合はいらない)

    Methods:
        lowest_common_ancestor(u, v): u, vの最小共通祖先を求める, O(log N)
        get_vertex_value(u): 頂点uの重みを返す, O(log N)
        add_vertex_value(u, w): 頂点uの重みにwを加算する (V_u += w), O(log N)
        update_vertex_value(u, w): 頂点uの重みをwに変更する (V_u = w), O(log N)
        vertex_sum(u, v): u -> v の頂点の重みの和を求める (u, vの重みも含む), O((log N)^2)
    """

    def __init__(
        self,
        graph: AdjacencyList,
        vertex_value: list[T],
        segfunc: Callable[[T, T], T],
        ide_ele: T,
        root: int = 0,
    ):
        """HL分解

        Args:
            graph (AdjacencyList): 木グラフ
            vertex_value (list[T]): 頂点の値
            segfunc (Callable[[T, T], T]): 2頂点の値をマージする関数
            ide_ele (T): segfuncに対する単位元
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
        # heavy_node_start_on_seg_tree[v]: SegmentTree上でのheavy_nodeの開始位置
        self.heavy_node_start_on_seg_tree = []

        self._build(graph, vertex_value, segfunc, ide_ele, root)

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

    def _build_segment_tree(
        self,
        vertex_value: list[T],
        segfunc: Callable[[T, T], T],
        ide_ele: T,
    ):
        """SegmentTreeの構築

        Args:
            vertex_value (list[T]): 頂点の値
            segfunc (Callable[[T, T], T]): 2頂点の値をマージする関数
            ide_ele (T): segfuncに対する単位元

        TimeComplexity:
            O(N logN)
        """
        seg_data = [vertex_value[v] for v in chain.from_iterable(self.heavy_node)]
        self.seg_tree1 = SegmentTree[T](seg_data, segfunc, ide_ele)
        self.seg_tree2 = SegmentTree[T](
            A=seg_data,
            segfunc=lambda x, y: segfunc(y, x),
            ide_ele=ide_ele,
        )

        s = 0
        for heavy in self.heavy_node:
            self.heavy_node_start_on_seg_tree.append(s)
            s += len(heavy)

    def _build(
        self,
        graph: AdjacencyList,
        vertex_value: list[T],
        segfunc: Callable[[T, T], T],
        ide_ele: T,
        root: int,
    ):
        """HL分解 & SegmentTreeの構築

        Args:
            graph (AdjacencyList): 木グラフ
            vertex_value (list[T]): 頂点の値
            segfunc (Callable[[T, T], T]): 2頂点の値をマージする関数
            ide_ele (T): segfuncに対する単位元
            root (int): 根とする頂点

        TimeComplexity:
            O(N logN)
        """
        heavy_child = self._calculate_heavy_child(graph, root)
        self._decompose(graph, root, heavy_child)
        self._build_segment_tree(vertex_value, segfunc, ide_ele)

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

    def _get_seg_tree_index(self, u: int) -> int:
        """SegmentTree上での頂点uのindexを返す

        Args:
            u (int): 頂点 (縮約前)

        Returns:
            int: SegmentTree上でのindex
        """
        heavy_node = self.heavy_node_mappings[u]
        head_ind = self.heavy_node_start_on_seg_tree[heavy_node]
        ind = head_ind + self.depth_on_heavy_path[u]
        return ind

    def get_vertex_value(self, u: int) -> T:
        """頂点uの値を返す

        Args:
            u (int): 頂点 (縮約前)

        Returns:
            T: 頂点uの値
        """
        return self.seg_tree1.get(self._get_seg_tree_index(u))

    def add_vertex_value(self, u: int, w: T):
        """頂点uの値にwを加算する (V_u += w)

        Args:
            u (int): 頂点 (縮約前)
            w (T): 加算値
        """
        self.seg_tree1.add(self._get_seg_tree_index(u), w)
        self.seg_tree2.add(self._get_seg_tree_index(u), w)

    def update_vertex_value(self, u: int, w: T):
        """頂点uの値をwに変更する (V_u = w)

        Args:
            u (int): 頂点 (縮約前)
            w (T): 変更値
        """
        self.seg_tree1.update(self._get_seg_tree_index(u), w)
        self.seg_tree2.update(self._get_seg_tree_index(u), w)

    def vertex_aggregation_value(self, u: int, v: int) -> T:
        """u -> v の頂点の値の集約値を求める (u, vの値も含む)

        Args:
            u (int): 頂点 (縮約前)
            v (int): 頂点 (縮約前)

        Returns:
            T: u -> v の頂点の値の集約値

        TimeComplexity:
            O((log N)^2)
        """
        s = self.seg_tree1.ide_ele

        lca = self.lowest_common_ancestor(u, v)
        heavy_lca = self.heavy_node_mappings[lca]

        heavy_u = self.heavy_node_mappings[u]
        heavy_v = self.heavy_node_mappings[v]

        # u -> lcaの集約値 (lcaを含まない)
        while heavy_u != heavy_lca:
            # u -> uが属するheadの頂点までの集約値
            head_ind = self.heavy_node_start_on_seg_tree[heavy_u]
            heavy_u_ind = head_ind + self.depth_on_heavy_path[u]
            s = self.seg_tree1.segfunc(
                s,
                self.seg_tree2.query(head_ind, heavy_u_ind + 1)
            )
            u = self.prev[self.heavy_node[heavy_u][0]]
            heavy_u = self.heavy_node_mappings[u]

        if u != lca:
            head_ind = self.heavy_node_start_on_seg_tree[heavy_u]
            lca_ind = head_ind + self.depth_on_heavy_path[lca]
            u_ind = head_ind + self.depth_on_heavy_path[u]
            # lcaを含めない
            s = self.seg_tree1.segfunc(
                s,
                self.seg_tree2.query(lca_ind + 1, u_ind + 1)
            )

        # lca -> vの集約値 (lcaを含む)
        # 最初にv -> lcaの区間を求める
        query_range = []
        while heavy_v != heavy_lca:
            head_ind = self.heavy_node_start_on_seg_tree[heavy_v]
            heavy_v_ind = head_ind + self.depth_on_heavy_path[v]
            query_range.append((head_ind, heavy_v_ind + 1))
            v = self.prev[self.heavy_node[heavy_v][0]]
            heavy_v = self.heavy_node_mappings[v]

        head_ind = self.heavy_node_start_on_seg_tree[heavy_u]
        lca_ind = head_ind + self.depth_on_heavy_path[lca]
        v_ind = head_ind + self.depth_on_heavy_path[v]
        query_range.append((lca_ind, v_ind + 1))

        for left, right in reversed(query_range):
            s = self.seg_tree1.segfunc(
                s,
                self.seg_tree1.query(left, right)
            )

        return s


def VertexSetPathComposite(
    graph: AdjacencyList,
    vertex_value: list[tuple[int, int]],
    root: int = 0,
    MOD: int = 1,
) -> HeavyLightDecompositionOnSegmentTree[tuple[int, int]]:
    """Vertex Set Path Composite

    Args:
        graph (AdjacencyList): 木
        vertex_value (list[tuple[int, int]]): [a, b] -> f(x) = a * x + b
        root (int, optional): 木の根. Defaults to 0.
        MOD (int): MOD

    Returns:
        HeavyLightDecompositionOnSegmentTree[tuple[int, int]]: Vertex Set Path Composite
    """
    return HeavyLightDecompositionOnSegmentTree[tuple[int, int]](
        graph=graph,
        vertex_value=vertex_value,
        segfunc=lambda x, y: ((y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD),
        ide_ele=(1, 0),
        root=root
    )
