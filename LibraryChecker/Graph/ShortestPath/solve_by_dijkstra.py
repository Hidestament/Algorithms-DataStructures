# https://judge.yosupo.jp/submission/158854

import sys

from src.Algorithms.Graph.ShortestPath.dijkstra import dijkstra
from src.Algorithms.Graph.ShortestPath.reconstruct_shortest_path import (
    reconstruct_shortest_path,
)


input = sys.stdin.readline

N, M, s, t = map(int, input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))

dist, prev = dijkstra(graph, s)

if dist[t] == float("INF"):
    print(-1)
    exit()

shortest_path = reconstruct_shortest_path(prev, s, t)
print(dist[t], len(shortest_path) - 1)
for u, v in zip(shortest_path, shortest_path[1:]):
    print(u, v)
