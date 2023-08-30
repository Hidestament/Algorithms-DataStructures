import sys

from DataStructures.BinaryTree.wavelet_matrix import WaveletMatrix

input = sys.stdin.readline


def compress(A):
    B = sorted(set(A))
    zipped = {}
    unzipped = {}
    for i, x in enumerate(B):
        zipped[x] = i
        unzipped[i] = x
    return zipped, unzipped


N, Q = map(int, input().split())
A = list(map(int, input().split()))

query = [tuple(map(int, input().split())) for _ in range(Q)]

zipped, unzipped = compress(A + [x for _, _, x in query])

wm = WaveletMatrix([zipped[x] for x in A])

for left, right, x in query:
    print(wm.range_freq(left, right, zipped[x], zipped[x] + 1))
