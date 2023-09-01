def reconstruct_shortest_path(prev: list[int], start: int, end: int) -> list[int]:
    """最短経路を復元する.

    Args:
        prev (list[int]): 先行頂点のリスト.
        start (int): 始点.
        end (int): 終点.

    Returns:
        list[int]: 最短経路.

    Note:
        - prevはstartから始まる経路を復元するためのものであること.
        - start - endは連結であること.
    """
    shortest_path = []
    now = end

    while True:
        shortest_path.append(now)

        if now == start:
            break

        now = prev[now]

    return shortest_path[::-1]
