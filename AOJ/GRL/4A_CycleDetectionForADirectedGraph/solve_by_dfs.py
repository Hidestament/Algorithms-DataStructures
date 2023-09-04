# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_4_A/judge/8240937/PyPy3

import sys

from Algorithms.Graph.CycleDetection.cycle_detection_by_dfs import cycle_detection


input = sys.stdin.readline

V, E = map(int, input().split())
graph = [[] for _ in range(V)]
for e in range(E):
    s, t = map(int, input().split())
    graph[s].append((t, e))

cycle_v, _ = cycle_detection(graph)
print(1 if cycle_v else 0)
