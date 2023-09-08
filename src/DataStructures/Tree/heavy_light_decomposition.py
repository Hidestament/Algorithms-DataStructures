import sys
from collections import deque

sys.setrecursionlimit(10**6)


class HeavyLightDecomposition:
    def __init__(self, graph, weight):
        """_summary_

        Args:
            graph (_type_): _description_
            weight (_type_): _description_

        最終的に持っとかなきゃいけないもの
        - prev
        - depth_on_path
        - segment_tree
        - heavy_node
        - heavy_node_depth
        - heavy_node_number
        """

        self.graph = graph
        self.weight = weight

        # prev[v]: vの先行頂点
        self.prev = [-1] * len(graph)
        # heavy_child[v]: 頂点vのheavyな子頂点
        self.heavy_child = [None] * len(graph)
        self._dfs()

        # depth_on_path[v]: 頂点vが属するheavy path上でのheadからの距離
        self.depth_on_path = [0] * len(graph)

        # 頂点の重みを(heavy_path)頂点ごとに固めて並べたもの (segment treeに乗せる)
        weight_on_segment_tree = []
        self.segment_tree_index = [-1] * len(graph)

        # 縮約後の頂点列
        self.heavy_node = []
        # 縮約御の頂点の深さ
        self.heavy_node_depth = []
        # concentration_vertex_numbers[v]: 頂点vが属する集約後の頂点番号
        self.heavy_node_number = [0] * len(graph)

        # (root, d): heavy_pathの根(始点), 深さ
        dq = deque([(0, 0)])
        while dq:
            # 最初に, vからheavy pathをたどる
            root, depth = dq.popleft()
            heavy_path = []

            now = root
            while now is not None:
                # nowに繋がるlightな頂点をdequeに入れる
                for to in self.graph[now]:
                    # 辿ってきたpath or heavyな頂点ならスキップ
                    if to == self.prev[now] or to == self.heavy_child[now]:
                        continue
                    dq.append((to, depth + 1))

                self.heavy_node_number[now] = len(self.heavy_node)
                weight_on_segment_tree.append(self.weight[now])
                self.segment_tree_index[now] = len(weight_on_segment_tree) - 1
                self.depth_on_path[now] = len(heavy_path)
                heavy_path.append(now)
                now = self.heavy_child[now]

            self.heavy_node.append(heavy_path)
            self.heavy_node_depth.append(depth)

    def _dfs(self, now=0, parent=-1):
        num_subtree = 1
        max_heavy_subtree_size = 0
        for to in self.graph[now]:
            if to == parent:
                continue
            self.prev[to] = now
            to_subtree_size = self._dfs(to, now)

            if to_subtree_size > max_heavy_subtree_size:
                max_heavy_subtree_size = to_subtree_size
                self.heavy_child[now] = to

            num_subtree += to_subtree_size

        return num_subtree

    def _head(self, v):
        # 頂点vが属するheavy pathの先頭 (最も根に近い頂点)
        heavy_node = self.heavy_node_number[v]
        return self.heavy_node[heavy_node][0]

    def update(self, v, w):
        ...

    def lowest_common_ancestor(self, u, v):
        # u, vの最小共通祖先を求める
        heavy_u = self.heavy_node_number[u]
        heavy_u_depth = self.heavy_node_depth[heavy_u]

        heavy_v = self.heavy_node_number[v]
        heavy_v_depth = self.heavy_node_depth[heavy_v]

        # vを深い方の頂点に統一する
        if heavy_u_depth > heavy_v_depth:
            u, v = v, u
            heavy_u, heavy_v = heavy_v, heavy_u
            heavy_u_depth, heavy_v_depth = heavy_v_depth, heavy_u_depth

        # vをuと同じ深さまで遡る
        for _ in range(heavy_v_depth - heavy_u_depth):
            head = self.heavy_node[heavy_v][0]
            v = self.prev[head]
            heavy_v = self.heavy_node_number[v]

        # u, vが同じ頂点になるまで遡る
        while heavy_u != heavy_v:
            u = self.prev[self.heavy_node[heavy_u][0]]
            heavy_u = self.heavy_node_number[u]
            v = self.prev[self.heavy_node[heavy_v][0]]
            heavy_v = self.heavy_node_number[v]

        # u, vが同じheavy pathにいるので, 根に近い方がLCA
        return u if self.depth_on_path[u] < self.depth_on_path[v] else v

    def dist_from_root(self, u):
        ...

    def dist(self, u, v):
        lca = self.lowest_common_ancestor(u, v)
        d = (
            self.dist_from_root(u)
            + self.dist_from_root(v)
            - 2 * self.dist_from_root(lca)
        )
        return d


input = sys.stdin.readline

N, Q = map(int, input().split())
P = list(map(int, input().split()))

graph = [[] for _ in range(N)]
for i, p in enumerate(P, start=1):
    # 頂点iの親がp
    graph[p].append(i)

aa = HeavyLightDecomposition(graph, [0] * N)

for _ in range(Q):
    u, v = map(int, input().split())
    print(aa.lowest_common_ancestor(u, v))
