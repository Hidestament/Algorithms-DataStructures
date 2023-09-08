# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_B/judge/8240445/PyPy3

import sys

from src.DataStructures.RangeTree.segment_tree import RangeSumQuery


input = sys.stdin.readline

N, Q = map(int, input().split())
seg = RangeSumQuery([0 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        i, x = query[1:]
        seg.add(i - 1, x)
    else:
        left, right = query[1:]
        print(seg.query(left - 1, right))
