################################################################################################################################
# Weighted Union Find Tree: 以下の操作を全て O(a(N)). aはアッカーマン関数の逆関数.
# union(x, y): xを含む集合とyを含む集合を重み w でmergeする
# find(x): xを含む集合を取得
# same_check(x, y): 要素x, yが同じ集合に属するかどうかの判定
# diff(x, y): yのxに対する相対的な重みを取得
# Note: 経路圧縮・Union By Rank が実装
################################################################################################################################

################################################################################################################################
# Verify
# ABC087 D - People on a Line (586ms): https://atcoder.jp/contests/abc087/submissions/30126227
# AOJ DSL_1_B (2.28s): https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/DSL_1_B/judge/6403657/Python3
################################################################################################################################

################################################################################################################################
# TODO
# 1. need refactoring
# 2. add docstring
################################################################################################################################


class WeightedUnionFindTree:
    def __init__(self, n):
        self.parents = [-1] * n
        # 親への相対的な重み
        self.weight = [0] * n

    def find(self, x):
        """
        x の root頂点を返す
        """
        if self.parents[x] < 0:
            return x
        else:
            # 繋ぎ変えてしまうので, 親の重みをweight[x]に追加する必要がある
            self.weight[x] += self.weight[self.parents[x]]
            # 繋ぎ変え
            self.parents[x] = self.find(self.parents[x])
            return self.find(self.parents[x])

    def union(self, x, y, w):
        """
        y の x に対する相対的な重みがwになるようにunionする
        つまり, diff(x, y) = w となる
        xとyがすでに同じグループの場合はFalseを返す
        """
        w += self.weight[x]  # xが基準となるので, weight[x]を加える
        w -= self.weight[y]  # xが基準となるので, yの重み分減らす

        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False

        # サイズが 小さい方 を 大きい方 へつなげる
        if self.parents[x] > self.parents[y]:
            x, y = y, x
            w *= -1

        # y を x の下にくっつける
        self.parents[x] += self.parents[y]  # サイズの更新
        self.parents[y] = x
        self.weight[y] = w
        return True

    def same_check(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        return -1 * self.parents[self.find(x)]

    def diff(self, x, y):
        """
        y の x に対する相対的な重みを取得
        """
        return self.weight[y] - self.weight[x]
