# https://judge.yosupo.jp/submission/158748

from src.Algorithms.Graph.CycleDetection.cycle_detection_by_dfs import cycle_detection


N, M = map(int, input().split())
graph = [[] for _ in range(N)]

for i in range(M):
    u, v = map(int, input().split())
    graph[u].append((v, i))
    graph[v].append((u, i))

cycle_v, cycle_e = cycle_detection(graph)

if cycle_v:
    print(len(cycle_v))
    print(*cycle_v)
    print(*cycle_e)
else:
    print(-1)
