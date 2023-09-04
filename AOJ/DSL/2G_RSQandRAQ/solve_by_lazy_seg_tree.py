# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_G/judge/8243568/PyPy3

import sys

from DataStructures.RangeTree.lazy_segment_tree import RangeSumRangeAdd


input = sys.stdin.readline

N, Q = map(int, input().split())
seg = RangeSumRangeAdd([0 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, x = query[1:]
        seg.range_update(left - 1, right, x)
    else:
        left, right = query[1:]
        print(seg.query(left - 1, right))
