# https://judge.yosupo.jp/submission/158510

from src.DataStructures.BinaryTree.wavelet_matrix import WaveletMatrix


N, Q = map(int, input().split())
A = list(map(int, input().split()))

wm = WaveletMatrix(A)

for _ in range(Q):
    left, right, k = map(int, input().split())
    print(wm.quantile(left, right, k + 1))
