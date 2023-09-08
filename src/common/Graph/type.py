# 隣接リスト
# ex. v0 - v1 - v2 = [[v1], [v0, v2], [v1]]
AdjacencyList = list[list[int]]

# 辺ナンバー付き隣接リスト
# ex. v0 -e0- v1 -e1- v2 = [[(v1, e0)], [(v0, e0), (v2, e1)], [(v1, e1)]]
AdjacencyListWithEdgeNumber = list[list[tuple[int, int]]]

# 重み付き隣接リスト
# ex v0 -(e0, w0)- v1 - (e1, w1) - v2 = [[(v1, w0)], [(v0, w0), (v2, w1)], [((v1, w1))]]
AdjacencyListWithWeight = list[list[tuple[int, int]]]

# 辺集合
# ex. v0 -e0- v1 -e1- v2 = [(v0, v1), (v1, v2)]
EdgeList = list[tuple[int, int]]

# 先行頂点列
# ex. v0 - v1 - v2 = [-1, v0, v1]
PreviousNodeList = list[int]
