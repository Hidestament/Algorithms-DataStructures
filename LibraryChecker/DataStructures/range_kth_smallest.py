from DataStructures.BinaryTree.wavelet_matrix import WaveletMatrix


N, Q = map(int, input().split())
A = list(map(int, input().split()))

wm = WaveletMatrix(A)

for _ in range(Q):
    l, r, k = map(int, input().split())
    print(wm.quantile(l, r, k + 1))
