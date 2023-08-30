from DataStructures.DisjointSet.union_find_tree import UnionFindTree


N, Q = map(int, input().split())
uf = UnionFindTree(N)

for _ in range(Q):
    t, u, v = map(int, input().split())

    if t == 0:
        uf.union(u, v)
    else:
        print(int(uf.same_check(u, v)))
