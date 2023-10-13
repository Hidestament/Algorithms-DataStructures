from src.Algorithms.NumberTheory.Prime.miller_rabin import miller_rabin


Q = int(input())
for _ in range(Q):
    n = int(input())
    print("Yes" if miller_rabin(n) else "No")
