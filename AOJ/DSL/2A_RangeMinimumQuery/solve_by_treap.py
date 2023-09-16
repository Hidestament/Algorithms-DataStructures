# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_A/judge/8289665/PyPy3

import sys

from src.DataStructures.BinarySearchTree.Treap.implicit_treap_recursion import RangeMinimumQuery


input = sys.stdin.readline

N, Q = map(int, input().split())
treap = RangeMinimumQuery([2**31 - 1 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        i, x = query[1:]
        treap[i] = x
    else:
        left, right = query[1:]
        print(treap.query(left, right + 1))
