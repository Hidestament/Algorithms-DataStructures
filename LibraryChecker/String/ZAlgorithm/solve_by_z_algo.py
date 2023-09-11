# https://judge.yosupo.jp/submission/160667

from src.Algorithms.String.z_algorithm import z_algorithm


S = str(input())
Z = z_algorithm(S)

print(*Z)
