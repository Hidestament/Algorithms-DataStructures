# https://judge.yosupo.jp/submission/161656
# https://judge.yosupo.jp/submission/161655

import sys

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeMinimumQuery


input = sys.stdin.readline


N, Q = map(int, input().split())
A = list(map(int, input().split()))

treap = RangeMinimumQuery(A)

for _ in range(Q):
    left, right = map(int, input().split())
    print(treap.query(left, right))
