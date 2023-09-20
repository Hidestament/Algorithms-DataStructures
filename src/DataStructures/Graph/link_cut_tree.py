from typing import TypeVar, Generic, Callable, Optional
from collections import deque
from array import array

from src.common.Graph.type import AdjacencyList, PreviousNodeList


V = TypeVar("V")


class LinkCutTree(Generic[V]):
    def __init__(
        self,
        graph: AdjacencyList,
        value: list[V],
        aggregate_func: Callable[[V, V], V],
        root: int = 0,
        prev: Optional[PreviousNodeList] = None,
    ):
        N = len(graph)

        # 超点数が多い場合には, "q" := long longにする
        self.left = array("l", [-1] * N)
        self.right = array("l", [-1] * N)
        self.parent = array("l", [-1] * N)
        # 反転フラグ
        self.reverse = array("b", [0] * N)
        self.value = [i for i in value]
        self.aggregation_value = [i for i in value]
        self.aggregate_func = aggregate_func
        self._build(graph, root, prev)

    def _bfs(self, graph: AdjacencyList, root: int) -> list[int]:
        """BFSで, 先行頂点 & rootからの距離を求める

        Args:
            graph (AdjacencyList): 木グラフ
            root (int): 根とする頂点

        Returns:
            list[int]: 先行頂点. rootの先行頂点は-1

        TimeComplexity:
            O(N)
        """
        N = len(graph)
        seen = [0] * N
        prev = [-1] * N

        dq = deque([(root, -1)])
        while dq:
            now, parent = dq.popleft()

            # 既に見た頂点なら
            if seen[now]:
                continue

            prev[now] = parent
            seen[now] = 1

            for to in graph[now]:
                if prev[to] != -1:
                    continue
                dq.append((to, now))

        return prev

    def _build(
        self,
        graph: AdjacencyList,
        root: int,
        prev: Optional[PreviousNodeList] = None
    ):
        """木を構築する

        Args:
            graph (AdjacencyList): 木グラフ
            root (int): 根とする頂点
            prev (Optional[PreviousNodeList]): 先行頂点.

        Notes:
            prevが与えられない場合は, BFSで求める
        """
        if prev is None:
            prev = self._bfs(graph, root)

        N = len(graph)
        for to in range(N):
            if prev[to] == -1:
                continue
            now = prev[to]
            self.link(now, to)

    def __getitem__(self, v: int) -> V:
        """value[v]を返す

        Args:
            v (int): 頂点番号

        Returns:
            V: value[v]
        """
        self.expose(v)
        return self.value[v]

    def __setitem__(self, v: int, value: V):
        """value[v] = valueに変更する

        Args:
            v (int): 頂点番号
            value (V): 変更値
        """
        self.update(v, value)

    def _is_root(self, v: int) -> bool:
        """vが部分木の根かどうかを判定する

        Args:
            v (int): 頂点番号

        Returns:
            bool: vが部分木の根ならTrue, そうでなければFalse
        """
        if self.parent[v] == -1:
            return True

        parent = self.parent[v]
        if (self.left[parent] == v) or (self.right[parent] == v):
            return False

        return True

    def _propagate(self, v: int):
        """vの情報を伝搬させる

        Args:
            v (int): 頂点番号
        """
        reverse = self.reverse
        # 反転フラグがない場合
        if not reverse[v]:
            return

        left, right = self.left, self.right
        left[v], right[v] = right[v], left[v]
        if left[v] != -1:
            reverse[left[v]] ^= 1
        if right[v] != -1:
            reverse[right[v]] ^= 1

        reverse[v] = 0

    def _update(self, v: int):
        """vの情報を更新する

        Args:
            v (int): 頂点番号
        """
        left, right = self.left[v], self.right[v]

        # 遅延情報の更新
        self._propagate(v)
        if left != -1:
            self._propagate(left)
        if right != -1:
            self._propagate(right)

        if (left == -1) and (right == -1):
            self.aggregation_value[v] = self.value[v]
        elif left == -1:
            self.aggregation_value[v] = self.aggregate_func(
                self.value[v],
                self.aggregation_value[right],
            )
        elif right == -1:
            self.aggregation_value[v] = self.aggregate_func(
                self.aggregation_value[left],
                self.value[v],
            )
        else:
            aggregation_value = self.aggregate_func(
                self.aggregation_value[left],
                self.value[v],
            )
            aggregation_value = self.aggregate_func(
                aggregation_value,
                self.aggregation_value[right],
            )
            self.aggregation_value[v] = aggregation_value

    def _rotate_right(self, node: int) -> int:
        """nodeを中心として右回転させる

        Args:
            node (int): 頂点番号

        Returns:
            int: 回転後の頂点番号

        Notes:
            0 <= node < N
        """
        left, right, parent = self.left, self.right, self.parent

        new_root = left[node]

        # 子の更新
        left[node] = right[new_root]
        right[new_root] = node

        # 親の更新
        parent[new_root] = parent[node]
        parent[node] = new_root
        if left[node] != -1:
            parent[left[node]] = node

        # new_rootの親の更新
        new_root_parent = parent[new_root]
        if (new_root_parent != -1) and (left[new_root_parent] == node):
            left[new_root_parent] = new_root
        elif (new_root_parent != -1) and (right[new_root_parent] == node):
            right[new_root_parent] = new_root

        # 値の更新
        self._update(node)
        self._update(new_root)
        return new_root

    def _rotate_left(self, node: int) -> int:
        """nodeを中心として左回転させる

        Args:
            node (int): 頂点番号

        Returns:
            int: 回転後の頂点番号

        Notes:
            0 <= node < N
        """
        left, right, parent = self.left, self.right, self.parent

        new_root = right[node]

        # 子の更新
        right[node] = left[new_root]
        left[new_root] = node

        # 親の更新
        parent[new_root] = parent[node]
        parent[node] = new_root
        if right[node] != -1:
            parent[right[node]] = node

        # new_rootの親の更新
        new_root_parent = parent[new_root]
        if (new_root_parent != -1) and (left[new_root_parent] == node):
            left[new_root_parent] = new_root
        elif (new_root_parent != -1) and (right[new_root_parent] == node):
            right[new_root_parent] = new_root

        # 値の更新
        self._update(node)
        self._update(new_root)
        return new_root

    def _splay(self, v: int):
        """vを根に持ってくる

        Args:
            v (int): 頂点番号
        """
        self._propagate(v)

        if self._is_root(v):
            return

        while not self._is_root(v):
            node = self.parent[v]
            parent = self.parent[node]

            # 伝播
            if parent != -1:
                self._propagate(parent)
            self._propagate(node)
            self._propagate(v)

            node_dir = self.left[node] == v
            # nodeがrootの場合
            if self._is_root(node):
                if node_dir:
                    self._rotate_right(node)
                else:
                    self._rotate_left(node)
                break

            parent_dir = self.left[parent] == node
            # zig-zig
            if node_dir == parent_dir:
                # 右回転
                if node_dir:
                    self._rotate_right(parent)
                    self._rotate_right(node)
                # 左回転
                else:
                    self._rotate_left(parent)
                    self._rotate_left(node)
            # zig-zag
            else:
                if node_dir:
                    self._rotate_right(node)
                    self._rotate_left(parent)
                else:
                    self._rotate_left(node)
                    self._rotate_right(parent)

    def root(self, v: int) -> int:
        """vの根を求める (元のグラフの根)

        Args:
            v (int): 頂点番号

        Returns:
            int: vの根
        """
        self.expose(v)
        left = self.left
        while left[v] != -1:
            v = left[v]
        self._splay(v)
        return v

    def is_same(self, u: int, v: int) -> bool:
        """uとvが同じ木に属しているかどうかを判定する

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Returns:
            bool: uとvが同じ木に属していればTrue, そうでなければFalse
        """
        return self.root(u) == self.root(v)

    def expose(self, v: int) -> int:
        """root -> vまでのパスを全て繋げる

        Args:
            v (int): 頂点番号

        Returns:
            int: splay前のrootの連結成分の根
        """
        prev_root = -1
        now_root = v

        while now_root != -1:
            self._splay(now_root)
            self.right[now_root] = prev_root
            self._update(now_root)
            now_root, prev_root = self.parent[now_root], now_root

        self._splay(v)
        return prev_root

    def link(self, u: int, v: int):
        """辺(u, v)を追加する

        Args:
            u (int): 頂点番号, 根に近い方の頂点.
            v (int): 頂点番号, 根から遠い方の頂点.

        Notes:
            辺(u, v)を追加しても, 木になっていることが前提
        """
        # u, vは異なる木なので, expose(u) -> uの右の子は存在しない
        # expose(v) -> vの左の子は存在しない
        self.expose(u)
        self.expose(v)

        self.right[u] = v
        self.parent[v] = u
        self._update(u)

    def cut(self, v: int):
        """辺(v, parent[v])を削除する

        Args:
            v (int): 頂点番号

        Notes:
            vに親がいることが前提
        """
        self.expose(v)

        v_left = self.left[v]
        self.parent[v_left] = -1
        self.left[v] = -1

        self._update(v)

    def evert(self, v: int):
        """頂点vを根にする

        Args:
            v (int): 頂点番号
        """
        self.expose(v)
        self.reverse[v] ^= 1
        self._propagate(v)

    def split(self, u: int, v: int):
        """頂点uとvを分離する

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Notes:
            u, vは同じ木に属していることが前提
            u, vの順序は関係ない
        """
        # uを根にする -> (u, v)の辺をカット
        self.evert(u)
        self.cut(v)

    def merge(self, u: int, v: int):
        """頂点uとvを併合する

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Notes:
            u, vは異なる木に属していることが前提
            u, vの順序は関係ない
        """
        # uを根にする -> uの親がいなくなる -> (v, u)を追加
        self.evert(u)
        self.link(v, u)

    def add(self, v: int, value: V):
        """value[v] += valueと加算する

        Args:
            v (int): 頂点番号
            value (V): 加算値

        Notes:
            型Vが, += に対応していないといけない
        """
        self.expose(v)
        self.value[v] += value
        self._update(v)

    def update(self, v: int, value: V):
        """value[v] = valueに変更する

        Args:
            v (int): 頂点番号
            value (V): 変更値
        """
        self.expose(v)
        self.value[v] = value
        self._update(v)

    def lowest_common_ancestor(self, u: int, v: int) -> Optional[int]:
        """uとvの最小共通祖先を求める

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Returns:
            Optional[int]: uとvの最小共通祖先. uとvが同じ木に属していない場合はNone
        """
        left = self.left

        self.expose(u)
        # 連結かどうか判定のために, rootまで辿って, rootが同じかどうか判定
        while left[u] != -1:
            u = left[u]

        lca = self.expose(v)
        while left[v] != -1:
            v = left[v]

        return lca if u == v else None

    def query(self, u: int, v: int) -> V:
        """uとvのパス上の集約値を求める

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Returns:
            V: uとvのパス上の集約値

        Notes:
            uとvが連結であることが前提
        """
        self.evert(u)
        self.expose(v)
        return self.aggregation_value[v]
