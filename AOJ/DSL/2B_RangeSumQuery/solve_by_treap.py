# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_B/judge/8289734/PyPy3

import sys

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeSumQuery


input = sys.stdin.readline

N, Q = map(int, input().split())
treap = RangeSumQuery([0 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        i, x = query[1:]
        treap.add(i - 1, x)
    else:
        left, right = query[1:]
        print(treap.query(left - 1, right))
