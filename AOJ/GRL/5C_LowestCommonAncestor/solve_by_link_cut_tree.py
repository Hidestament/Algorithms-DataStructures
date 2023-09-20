# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_5_C/judge/8301007/PyPy3
# src/Algorithms/Graph/LowestCommonAncestors/link_cut_tree.pyを修正したもの

import sys
from collections import deque


AdjacencyList = list[list[int]]


class LinkCutTree:
    """LCAのためのLink-Cut-Tree
    """

    def __init__(
        self,
        graph: AdjacencyList,
        root: int = 0,
    ):
        N = len(graph)

        self.left = [-1] * N
        self.right = [-1] * N
        self.parent = [-1] * N
        self._build(graph, root)

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
        prev = [-1] * N

        dq = deque([(root, -1)])
        while dq:
            now, parent = dq.popleft()

            # 既に見た頂点なら
            if prev[now] != -1:
                continue

            prev[now] = parent

            for to in graph[now]:
                if prev[to] != -1:
                    continue
                dq.append((to, now))

        return prev

    def _build(self, graph: AdjacencyList, root: int):
        """木を構築する

        Args:
            graph (AdjacencyList): 木グラフ
            root (int): 根とする頂点
        """
        prev = self._bfs(graph, root)

        N = len(graph)
        for to in range(N):
            if prev[to] == -1:
                continue
            now = prev[to]
            self.link(now, to)

    def is_root(self, v: int) -> bool:
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
        return new_root

    def _splay(self, v: int):
        """vを根に持ってくる

        Args:
            v (int): 頂点番号
        """
        if self.is_root(v):
            return

        while not self.is_root(v):
            node = self.parent[v]
            node_dir = self.left[node] == v

            # nodeがrootの場合
            if self.is_root(node):
                if node_dir:
                    self._rotate_right(node)
                else:
                    self._rotate_left(node)
                break

            parent = self.parent[node]
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
            now_root, prev_root = self.parent[now_root], now_root

        self._splay(v)
        return prev_root

    def link(self, u: int, v: int):
        """辺(u, v)を追加する

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Notes:
            辺(u, v)を追加しても, 木になっていることが前提
        """
        # u, vは異なる木なので, expose(u) -> uの右の子は存在しない
        # expose(v) -> vの左の子は存在しない
        self.expose(u)
        self.expose(v)

        self.right[u] = v
        self.parent[v] = u

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

    def lowest_common_ancestor(self, u: int, v: int) -> int:
        """uとvの最小共通祖先を求める (u, vが連結であることが前提)

        Args:
            u (int): 頂点番号
            v (int): 頂点番号

        Returns:
            int: uとvの最小共通祖先.
        """
        self.expose(u)
        lca = self.expose(v)
        return lca


input = sys.stdin.readline

N = int(input())

graph = [[] for _ in range(N)]
for parent in range(N):
    k, *v = map(int, input().split())
    for child in v:
        graph[parent].append(child)

hl = LinkCutTree(graph)

Q = int(input())
for _ in range(Q):
    u, v = map(int, input().split())
    print(hl.lowest_common_ancestor(u, v))
