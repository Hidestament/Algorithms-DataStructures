# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_H/judge/8243561/PyPy3

import sys

from DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeAdd


input = sys.stdin.readline

N, Q = map(int, input().split())
seg = RangeMinimumRangeAdd([0 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, x = query[1:]
        seg.range_update(left, right + 1, x)
    else:
        left, right = query[1:]
        print(seg.query(left, right + 1))
