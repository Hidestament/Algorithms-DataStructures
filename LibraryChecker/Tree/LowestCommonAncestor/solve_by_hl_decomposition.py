# https://judge.yosupo.jp/submission/160069

import sys

from src.Algorithms.Graph.LowestCommonAncestors.heavy_light_decomposition import (
    HeavyLightDecomposition,
)


input = sys.stdin.readline

N, Q = map(int, input().split())
P = list(map(int, input().split()))

graph = [[] for _ in range(N)]
for i, p in enumerate(P, start=1):
    # 頂点iの親がp
    graph[p].append(i)

hl = HeavyLightDecomposition(graph)

for _ in range(Q):
    u, v = map(int, input().split())
    print(hl.lowest_common_ancestor(u, v))
