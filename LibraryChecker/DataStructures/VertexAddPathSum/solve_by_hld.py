# https://judge.yosupo.jp/submission/160176

import sys

from src.DataStructures.Graph.heavy_light_decomposition_on_bit import HeavyLightDecompositionOnBIT


input = sys.stdin.readline

N, Q = map(int, input().split())
A = list(map(int, input().split()))
graph = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

hl = HeavyLightDecompositionOnBIT(graph, A)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        p, x = query[1:]
        hl.add_vertex_weight(p, x)
    else:
        u, v = query[1:]
        print(hl.vertex_sum(u, v))
