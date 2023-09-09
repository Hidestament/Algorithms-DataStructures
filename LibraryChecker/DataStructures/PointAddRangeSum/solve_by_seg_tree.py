# https://judge.yosupo.jp/submission/159028

import sys

from src.DataStructures.RangeTree.segment_tree import RangeSumQuery


input = sys.stdin.readline

N, Q = map(int, input().split())
A = list(map(int, input().split()))

seg = RangeSumQuery(A)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        p, x = query[1:]
        seg.add(p, x)
    else:
        left, right = query[1:]
        print(seg.query(left, right))
