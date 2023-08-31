from DataStructures.DisjointSet.union_find_tree import UnionFindTree


def undirected_cycle_detection_by_uf(
    num_vertex: int,
    edges: list[tuple[int, int]],
) -> bool:
    """単純無向グラフにおいて閉路が存在するかどうかを判定する. UnionFindTreeを使用. 復元はできない.

    Args:
        num_vertex (int): 頂点の個数N.
        edges (list[tuple[int, int]]): 辺のリスト. 0-indexed.

    Returns:
        bool: True -> 閉路が存在する, False -> 閉路が存在しない

    TimeComplexity:
        O(N + Mα(N)) (αはアッカーマン関数)
    """
    uf = UnionFindTree(num_vertex)

    for u, v in edges:
        if uf.same_check(u, v):
            return True
        uf.union(u, v)

    return False
