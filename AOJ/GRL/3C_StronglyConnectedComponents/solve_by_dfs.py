# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_3_C/judge/8271138/PyPy3

import sys

from src.Algorithms.Graph.StronglyConnectedComponents.strongly_connected_components import strongly_connected_components


input = sys.stdin.readline

N, M = map(int, input().split())
graph = [[] for _ in range(N)]
reverse_graph = [[] for _ in range(N)]

for _ in range(M):
    s, t = map(int, input().split())
    graph[s].append(t)
    reverse_graph[t].append(s)

scc = strongly_connected_components(graph, reverse_graph)
labels = [-1] * N

for i, component in enumerate(scc):
    for v in component:
        labels[v] = i

Q = int(input())
for _ in range(Q):
    u, v = map(int, input().split())
    print(1 if labels[u] == labels[v] else 0)
