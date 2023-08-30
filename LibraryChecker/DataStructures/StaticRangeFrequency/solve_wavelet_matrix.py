from DataStructures.BinaryTree.wavelet_matrix import WaveletMatrix


N, Q = map(int, input().split())
A = list(map(int, input().split()))

wm = WaveletMatrix(A)

for _ in range(Q):
    l, r, x = map(int, input().split())
    print(wm.range_freq(l, r, x, x + 1))
