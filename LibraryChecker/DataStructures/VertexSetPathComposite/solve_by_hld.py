# https://judge.yosupo.jp/submission/160219

import sys

from src.DataStructures.Graph.heavy_light_decomposition_on_seg_tree import VertexSetPathComposite


input = sys.stdin.readline
MOD = 998244353


N, Q = map(int, input().split())
A = [tuple(map(int, input().split())) for _ in range(N)]

graph = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

hld = VertexSetPathComposite(graph, A, MOD=MOD)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        p, c, d = query[1:]
        hld.update_vertex_value(p, (c, d))
    else:
        u, v, x = query[1:]
        func = hld.vertex_aggregation_value(u, v)
        print((func[0] * x + func[1]) % MOD)
