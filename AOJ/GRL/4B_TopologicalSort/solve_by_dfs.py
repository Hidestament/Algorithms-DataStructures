# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/GRL_4_B/judge/8271193/PyPy3

import sys

from src.Algorithms.Graph.TopologicalSort.topological_sort import topological_sort


input = sys.stdin.readline

N, M = map(int, input().split())
graph = [[] for _ in range(N)]
indegree = [0] * N

for _ in range(M):
    s, t = map(int, input().split())
    graph[s].append(t)
    indegree[t] += 1

print(*topological_sort(graph, indegree), sep="\n")
