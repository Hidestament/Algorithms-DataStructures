# https://judge.yosupo.jp/submission/160825

import sys

from src.Algorithms.Graph.StronglyConnectedComponents.strongly_connected_components \
    import strongly_connected_components
from src.Algorithms.Graph.StronglyConnectedComponents.construct import construct
from src.Algorithms.Graph.TopologicalSort.topological_sort import topological_sort


input = sys.stdin.readline

N, M = map(int, input().split())

graph = [[] for _ in range(N)]
reverse_graph = [[] for _ in range(N)]
for _ in range(M):
    a, b = map(int, input().split())
    graph[a].append(b)
    reverse_graph[b].append(a)

scc = strongly_connected_components(graph, reverse_graph)
scc_graph = construct(graph, scc)

scc_indegree = [0] * len(scc_graph)
for u in range(len(scc)):
    for v in scc_graph[u]:
        scc_indegree[v] += 1

topological_order = topological_sort(scc_graph, scc_indegree)

print(len(topological_order))
for v in topological_order:
    print(len(scc[v]), *scc[v])
