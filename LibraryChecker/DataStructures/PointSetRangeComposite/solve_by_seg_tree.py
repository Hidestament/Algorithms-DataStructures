# https://judge.yosupo.jp/submission/159029

import sys

from DataStructures.RangeTree.segment_tree import SegmentTree


input = sys.stdin.readline


MOD = 998244353
N, Q = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(N)]

seg = SegmentTree(
    N=N,
    segfunc=lambda x, y: [(y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD],
    ide_ele=[1, 0],
)
for i, a in enumerate(A):
    seg[i] = a

print(seg.tree)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        p, c, d = query[1:]
        seg[p] = [c, d]
    else:
        left, right, x = query[1:]
        f = seg.query(left, right)
        print((f[0] * x + f[1]) % MOD)
