#########################################################################################
# Union Find Tree: 以下の操作を全て O(a(N)). aはアッカーマン関数の逆関数.
# union(x, y): xを含む集合とyを含む集合をmergeする
# find(x): 要素xを含む集合を取得
# size(x): 要素xを含む集合の要素数を取得
# same_check(x, y): 要素x, yが同じ集合に属するかどうかの判定
# Note: 経路圧縮・Union By Rank が実装さ
#########################################################################################

#########################################################################################
# Verify
# Library Checker - Unionfind (582ms): https://judge.yosupo.jp/submission/72696
#########################################################################################

#########################################################################################
# TODO
# 1. add docstring
#########################################################################################


class UnionFindTree:
    def __init__(self, n):
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.find(self.parents[x])

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def same_check(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        return -1 * self.parents[self.find(x)]
