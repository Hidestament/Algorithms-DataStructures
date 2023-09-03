# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_E/judge/8240386/Python3

from DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeAdd


N, Q = map(int, input().split())
A = [0] * N

seg = RangeMinimumRangeAdd(A)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, x = query[1:]
        seg.range_update_recursion(left - 1, right, x)
    else:
        i = query[1]
        print(seg[i - 1])
