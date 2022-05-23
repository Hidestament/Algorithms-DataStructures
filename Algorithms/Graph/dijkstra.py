from heapq import heappush, heappop


class Graph:
    def __init__(self, N: int, M: int, directed: bool = False, weighted: bool = False):
        self.num_ver = N
        self.num_edge = M
        self.adj_list = [[] for _ in range(N)]
        for _ in range(M):
            edges = list(map(int, input().split()))
            u, v = edges[0], edges[1]
            cost = edges[-1] if weighted else 1
            self.adj_list[u - 1].append([v - 1, cost])
            if not directed:
                self.adj_list[v - 1].append([u - 1, cost])

    def dijkstra(self, start: int = 0):
        INF = 10**15
        dist = [INF] * self.num_ver
        flag = [0] * self.num_ver
        dist[start] = 0
        flag[start] = 1
        hq = [[0, start]]
        while hq:
            _, now = heappop(hq)
            if flag[now]:
                continue
            flag[now] = 1
            for to, cost in self.adj_list[now]:
                if flag[to]:
                    continue
                if dist[to] < dist[now] + cost:
                    continue
                dist[to] = dist[now] + cost
                heappush(hq, [dist[to], to])

        return dist
