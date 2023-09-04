# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_1_A/judge/8240932/PyPy3

import sys

from Algorithms.Graph.ShortestPath.dijkstra import dijkstra


input = sys.stdin.readline

V, E, start = map(int, input().split())
graph = [[] for _ in range(V)]
for _ in range(E):
    s, t, d = map(int, input().split())
    graph[s].append((t, d))


dist, _ = dijkstra(graph, start)
for d in dist:
    print(d if d != float("INF") else "INF")
