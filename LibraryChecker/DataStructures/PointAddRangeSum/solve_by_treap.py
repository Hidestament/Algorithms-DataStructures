# 再帰なので遅いTLE
# https://judge.yosupo.jp/submission/161652
# https://judge.yosupo.jp/submission/161654

import sys

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeSumQuery


input = sys.stdin.readline

N, Q = map(int, input().split())
A = list(map(int, input().split()))

treap = RangeSumQuery(A)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        p, x = query[1:]
        treap.add(p, x)
    else:
        left, right = query[1:]
        print(treap.query(left, right))
