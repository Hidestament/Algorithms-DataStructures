# https://judge.yosupo.jp/submission/158749

from Algorithms.Graph.CycleDetection.cycle_detection_by_dfs import cycle_detection


N, M = map(int, input().split())
graph = [[] for _ in range(N)]

for i in range(M):
    u, v = map(int, input().split())
    graph[u].append((v, i))

_, cycle_e = cycle_detection(graph)

if cycle_e:
    print(len(cycle_e))
    print(*cycle_e, sep="\n")
else:
    print(-1)
