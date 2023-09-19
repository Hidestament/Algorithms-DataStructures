# https://judge.yosupo.jp/submission/162129

import sys

from src.DataStructures.BinarySearchTree.SplayTree.splay_hash_map_fast import SplayHashMap


input = sys.stdin.readline

Q = int(input())
tree = SplayHashMap[int, int]()

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        k, v = query[1:]
        tree[k] = v
    else:
        k = query[1]
        print(tree.get(k, 0))
