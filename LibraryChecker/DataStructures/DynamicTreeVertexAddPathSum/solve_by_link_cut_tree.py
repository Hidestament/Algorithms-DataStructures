# Pythonじゃ無理
# https://judge.yosupo.jp/submission/162245
# src/DataStructures/Graph/link_cut_tree.py を修正したもの

import sys

from collections import deque
from array import array


input = sys.stdin.readline

N, Q = map(int, input().split())
A = list(map(int, input().split()))

graph = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)


left = array("l", [-1] * N)
right = array("l", [-1] * N)
parent = array("l", [-1] * N)
reverse = array("b", [0] * N)
value = array("l", A)
aggregation_value = array("l", A)


def _bfs(graph) -> list[int]:
    N = len(graph)
    seen = [0] * N
    prev = [-1] * N

    dq = deque([(0, -1)])
    while dq:
        now, parent = dq.popleft()

        # 既に見た頂点なら
        if seen[now]:
            continue

        prev[now] = parent
        seen[now] = 1

        for to in graph[now]:
            if prev[to] != -1:
                continue
            dq.append((to, now))

    return prev


def _build(graph):
    prev = _bfs(graph)
    N = len(graph)
    for to in range(N):
        if prev[to] == -1:
            continue
        now = prev[to]
        link(now, to)


def _is_root(v: int) -> bool:
    if parent[v] == -1:
        return True

    parent_node = parent[v]
    if (left[parent_node] == v) or (right[parent_node] == v):
        return False

    return True


def _propagate(v: int):
    """vの情報を伝搬させる
    Args:
        v (int): 頂点番号
    """
    # 反転フラグがない場合
    if reverse[v] == 0:
        return
    left[v], right[v] = right[v], left[v]
    if left[v] != -1:
        reverse[left[v]] ^= 1
    if right[v] != -1:
        reverse[right[v]] ^= 1
    reverse[v] = 0


def _update(v: int):
    """vの情報を更新する
    Args:
        v (int): 頂点番号
    """
    left_node = left[v]
    right_node = right[v]

    # 遅延情報の更新
    _propagate(v)
    if left_node != -1:
        _propagate(left_node)
    if right_node != -1:
        _propagate(right_node)

    if left_node == -1:
        left_value = 0
    else:
        left_value = aggregation_value[left_node]

    if right_node == -1:
        right_value = 0
    else:
        right_value = aggregation_value[right_node]

    aggregation_value[v] = left_value + value[v] + right_value


def _rotate_right(node: int) -> int:
    """nodeを中心として右回転させる
    Args:
        node (int): 頂点番号
    Returns:
        int: 回転後の頂点番号
    Notes:
        0 <= node < N
    """
    new_root = left[node]

    # 子の更新
    left[node] = right[new_root]
    right[new_root] = node

    # 親の更新
    parent[new_root] = parent[node]
    parent[node] = new_root

    if left[node] != -1:
        parent[left[node]] = node

    # new_rootの親の更新
    new_root_parent = parent[new_root]
    if (new_root_parent != -1) and (left[new_root_parent] == node):
        left[new_root_parent] = new_root
    elif (new_root_parent != -1) and (right[new_root_parent] == node):
        right[new_root_parent] = new_root

    # 値の更新
    _update(node)
    _update(new_root)
    return new_root


def _rotate_left(node: int) -> int:
    """nodeを中心として左回転させる

    Args:
        node (int): 頂点番号

    Returns:
        int: 回転後の頂点番号

    Notes:
        0 <= node < N
    """
    new_root = right[node]

    # 子の更新
    right[node] = left[new_root]
    left[new_root] = node

    # 親の更新
    parent[new_root] = parent[node]
    parent[node] = new_root
    if right[node] != -1:
        parent[right[node]] = node

    # new_rootの親の更新
    new_root_parent = parent[new_root]
    if (new_root_parent != -1) and (left[new_root_parent] == node):
        left[new_root_parent] = new_root
    elif (new_root_parent != -1) and (right[new_root_parent] == node):
        right[new_root_parent] = new_root

    # 値の更新
    _update(node)
    _update(new_root)
    return new_root


def _splay(v: int):
    """vを根に持ってくる

    Args:
        v (int): 頂点番号
    """
    _propagate(v)

    if _is_root(v):
        return

    while not _is_root(v):
        node = parent[v]
        parent_node = parent[node]

        # 伝播
        if parent_node != -1:
            _propagate(parent_node)

        _propagate(node)
        _propagate(v)

        node_dir = left[node] == v

        # nodeがrootの場合
        if _is_root(node):
            if node_dir:
                _rotate_right(node)
            else:
                _rotate_left(node)
            break

        parent_dir = left[parent_node] == node
        # zig-zig
        if node_dir == parent_dir:
            # 右回転
            if node_dir:
                _rotate_right(parent_node)
                _rotate_right(node)
            # 左回転
            else:
                _rotate_left(parent_node)
                _rotate_left(node)
        # zig-zag
        else:
            if node_dir:
                _rotate_right(node)
                _rotate_left(parent_node)
            else:
                _rotate_left(node)
                _rotate_right(parent_node)


def expose(v: int) -> int:
    """root -> vまでのパスを全て繋げる

    Args:
        v (int): 頂点番号

    Returns:
        int: splay前のrootの連結成分の根
    """
    prev_root = -1
    now_root = v

    while now_root != -1:
        _splay(now_root)
        right[now_root] = prev_root
        _update(now_root)
        now_root, prev_root = parent[now_root], now_root

    _splay(v)
    return prev_root


def link(u: int, v: int):
    """辺(u, v)を追加する

    Args:
        u (int): 頂点番号, 根に近い方の頂点.
        v (int): 頂点番号, 根から遠い方の頂点.

    Notes:
        辺(u, v)を追加しても, 木になっていることが前提
    """
    # u, vは異なる木なので, expose(u) -> uの右の子は存在しない
    # expose(v) -> vの左の子は存在しない
    expose(u)
    expose(v)
    right[u] = v
    parent[v] = u
    _update(u)


def cut(v: int):
    """辺(v, parent[v])を削除する
    Args:
        v (int): 頂点番号
    Notes:
        vに親がいることが前提
    """
    expose(v)
    v_left = left[v]
    parent[v_left] = -1
    left[v] = -1
    _update(v)


def evert(v: int):
    """頂点vを根にする
    Args:
        v (int): 頂点番号
    """
    expose(v)
    reverse[v] ^= 1
    _propagate(v)


def split(u: int, v: int):
    """頂点uとvを分離する
    Args:
        u (int): 頂点番号
        v (int): 頂点番号
    Notes:
        u, vは同じ木に属していることが前提
        u, vの順序は関係ない
    """
    # uを根にする -> (u, v)の辺をカット
    evert(u)
    cut(v)


def merge(u: int, v: int):
    """頂点uとvを併合する
    Args:
        u (int): 頂点番号
        v (int): 頂点番号
    Notes:
        u, vは異なる木に属していることが前提
        u, vの順序は関係ない
    """
    # uを根にする -> uの親がいなくなる -> (v, u)を追加
    evert(u)
    link(v, u)


def add(v: int, x: int):
    """value[v] += xと加算する

    Args:
        v (int): 頂点番号
        x (V): 加算値

    Notes:
        型Vが, += に対応していないといけない
    """
    expose(v)
    value[v] += x
    _update(v)


def query(u: int, v: int):
    """uとvのパス上の集約値を求める
    Args:
        u (int): 頂点番号
        v (int): 頂点番号
    Returns:
        V: uとvのパス上の集約値
    Notes:
        uとvが連結であることが前提
    """
    evert(u)
    expose(v)
    return aggregation_value[v]


_build(graph)

ans = []
for _ in range(Q):
    q = list(map(int, input().split()))
    if q[0] == 0:
        u, v, w, x = q[1:]
        split(u, v)
        merge(w, x)
    elif q[0] == 1:
        p, x = q[1:]
        add(p, x)
    else:
        u, v = q[1:]
        ans.append(query(u, v))

print(*ans, sep="\n")
