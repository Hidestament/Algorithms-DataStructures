# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_D/judge/8243533/PyPy3

from DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeUpdate


N, Q = map(int, input().split())
A = [pow(2, 31) - 1 for _ in range(N)]

seg = RangeMinimumRangeUpdate(A)
for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, x = query[1:]
        seg.range_update(left, right + 1, x)
    else:
        i = query[1]
        print(seg[i])
