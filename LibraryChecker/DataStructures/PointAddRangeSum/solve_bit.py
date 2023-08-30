from DataStructures.RangeTree.binary_indexed_tree import BinaryIndexedTree


N, Q = map(int, input().split())
A = list(map(int, input().split()))

bit = BinaryIndexedTree(N + 1)
for i, a in enumerate(A):
    bit.add(i, a)

for _ in range(Q):
    q = list(map(int, input().split()))
    if q[0] == 0:
        p, x = q[1], q[2]
        bit.add(p, x)
    else:
        left, right = q[1], q[2]
        print(bit.sum_range(left, right))
