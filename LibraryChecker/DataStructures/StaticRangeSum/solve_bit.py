# https://judge.yosupo.jp/submission/158575

from src.DataStructures.RangeTree.binary_indexed_tree import BinaryIndexedTree


N, Q = map(int, input().split())
A = list(map(int, input().split()))

bit = BinaryIndexedTree(N)
for i, a in enumerate(A):
    bit.add(i, a)

for _ in range(Q):
    left, right = map(int, input().split())
    print(bit.sum_range(left, right))
