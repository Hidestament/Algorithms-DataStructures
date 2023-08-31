# ex. v0 -e0- v1 -e1- v2 = [[(v0, e0)], [(v0, e0), (v2, e1)], [(v1, e1)]]
AdjacencyListWithEdgeNumber = list[list[tuple[int, int]]]

# ex. v0 -e0- v1 -e1- v2 = [(v0, v1), (v1, v2)]
EdgeList = list[tuple[int, int]]
