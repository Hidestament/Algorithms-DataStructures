# https://judge.yosupo.jp/submission/158955

from DataStructures.RangeTree.segment_tree import SegmentTree


N, Q = map(int, input().split())
A = list(map(int, input().split()))

seg = SegmentTree(N, min, float("inf"))
for i, a in enumerate(A):
    seg.update(i, a)

for _ in range(Q):
    left, right = map(int, input().split())
    print(seg.query(left, right))
