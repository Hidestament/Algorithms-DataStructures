from typing import Optional


class WeightedUnionFindTree:
    """根と各頂点の相対的な重みを管理するUnion Find Tree. 以下の操作を O(a(N)) で実行する

    Attributes:
        parents (list[int]): 頂点vの親
        diff_weight (list[int]): 頂点vの親からの相対的な重み

    Methods:
        union(x, y, w): xに対するyの相対的な重みがwとなるようにmergeする
        find(x): 要素xを含む集合を取得
        size(x): 要素xを含む集合の要素数を取得
        same_check(x, y): 要素x, yが同じ集合に属するかどうかの判定
        diff(x, y): xに対するyの重みを返す
    """

    def __init__(self, n: int):
        """コンストラクタ.

        Args:
            n (int): 要素数の最大値
        """
        self.parents: list[int] = [-1] * n
        self.diff_weight: list[int] = [0] * n

    def find(self, x: int) -> int:
        """xのrootの頂点を探す

        Args:
            x (int): 探す頂点

        Returns:
            int: xの親頂点

        Note:
            経路圧縮を行っている
        """
        if self.parents[x] < 0:
            return x

        root = self.find(self.parents[x])
        # 繋ぎ変えてしまうので, 親の重みをweight[x]に追加する
        self.diff_weight[x] += self.diff_weight[self.parents[x]]
        # 繋ぎ変え
        self.parents[x] = root
        return root

    def union(self, x: int, y: int, w: int) -> bool:
        """xに対するyの相対的な重みがwとなるように, xの属する集合と, yの属する集合を合併する
        つまり, weight[y] = weight[x] + w となる.

        Args:
            x (int): 集合の要素
            y (int): 集合の要素
            w (int): xに対するyの重み

        Returns:
            bool: True -> unionできたとき, False -> x, yが既に同じ集合のとき

        Note:
            Union By Rankで実装
        """
        # 経路圧縮
        self.find(x)
        self.find(y)

        # xが基準となるので, weight[x]を加え, weigh[y]を引く
        w = w + self.diff_weight[x] - self.diff_weight[y]

        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        # サイズが小さい方をy, 大きい方をxとする
        if self.size(rx) < self.size(ry):
            rx, ry = ry, rx
            w *= -1

        # y を x の下にくっつける
        self.parents[rx] += self.parents[ry]
        self.parents[ry] = rx
        self.diff_weight[ry] = w
        return True

    def same_check(self, x: int, y: int) -> bool:
        """xとyが同じ集合に属しているかを判定

        Args:
            x (int): 集合に属する要素
            y (int): 集合に属する要素

        Returns:
            bool: 同じ集合に属するかどうか
        """
        return self.find(x) == self.find(y)

    def diff(self, x: int, y: int) -> Optional[int]:
        """xに対するyの重みを返す

        Args:
            x (int): 集合の要素
            y (int): 集合の要素

        Returns:
            Optional[int]: xに対するyの重み. x, yが違う集合のときはNone.
        """
        if self.same_check(x, y) is False:
            return None

        # x, yを根の子に経路圧縮
        self.find(x)
        self.find(y)

        return self.diff_weight[y] - self.diff_weight[x]

    def size(self, x: int) -> int:
        """xが属する集合の要素数を返す

        Args:
            x (int): 集合に属する要素

        Returns:
            int: xが属する集合の要素数
        """
        return -1 * self.parents[self.find(x)]
