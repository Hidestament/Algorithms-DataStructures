# https://judge.yosupo.jp/submission/160854

import sys

from src.DataStructures.Set.multi_set import MultiSet


input = sys.stdin.readline


N, Q = map(int, input().split())
_S = list(map(int, input().split()))

S = MultiSet()
for s in _S:
    S.insert(s)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        x = query[1]
        S.insert(x)
    elif query[0] == 1:
        print(f"{S.pop_min()}")
    else:
        print(f"{S.pop_max()}")
