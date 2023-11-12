# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_1_B/judge/8483454/Python3

from src.DataStructures.DisjointSet.weighted_union_find_tree import WeightedUnionFindTree


N, Q = map(int, input().split())


uf = WeightedUnionFindTree(N)
for _ in range(Q):
    q = list(map(int, input().split()))
    if q[0] == 0:
        x, y, z = q[1:]
        if uf.same_check(x, y):
            continue
        else:
            uf.union(x, y, z)
    else:
        x, y = q[1:]
        if uf.same_check(x, y):
            print(uf.diff(x, y))
        else:
            print("?")
