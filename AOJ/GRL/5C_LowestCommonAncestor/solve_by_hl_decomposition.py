# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_5_C/judge/8267789/PyPy3

import sys

from src.Algorithms.Graph.LowestCommonAncestors.heavy_light_decomposition import HeavyLightDecomposition


input = sys.stdin.readline

N = int(input())

graph = [[] for _ in range(N)]
for parent in range(N):
    k, *v = map(int, input().split())
    for child in v:
        graph[parent].append(child)

hl = HeavyLightDecomposition(graph)

Q = int(input())
for _ in range(Q):
    u, v = map(int, input().split())
    print(hl.lowest_common_ancestor(u, v))
