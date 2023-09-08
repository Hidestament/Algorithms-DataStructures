# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_2_F/judge/8243546/PyPy3

from src.DataStructures.RangeTree.lazy_segment_tree import RangeMinimumRangeUpdate


N, Q = map(int, input().split())
seg = RangeMinimumRangeUpdate([pow(2, 31) - 1 for _ in range(N)])

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, x = query[1:]
        seg.range_update(left, right + 1, x)
    else:
        left, right = query[1:]
        print(seg.query(left, right + 1))
