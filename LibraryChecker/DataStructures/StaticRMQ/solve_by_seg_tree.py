# https://judge.yosupo.jp/submission/158955

from src.DataStructures.RangeTree.segment_tree import RangeMinimumQuery


N, Q = map(int, input().split())
A = list(map(int, input().split()))

seg = RangeMinimumQuery(A)

for _ in range(Q):
    left, right = map(int, input().split())
    print(seg.query(left, right))
