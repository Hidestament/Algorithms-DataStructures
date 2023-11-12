class UnionFindTree:
    """Union Find Tree. 以下の操作を O(a(N)) で実行する

    Methods:
        union(x, y): xを含む集合とyを含む集合をmergeする O(a(N))
        find(x): 要素xを含む集合を取得 O(a(N))
        size(x): 要素xを含む集合の要素数を取得 O(a(N))
        same_check(x, y): 要素x, yが同じ集合に属するかどうかの判定 O(a(N))
    """

    def __init__(self, n: int):
        """コンストラクタ.

        Args:
            n (int): 要素数の最大値
        """
        self.parents = [-1] * n

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
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.find(self.parents[x])

    def union(self, x: int, y: int) -> None:
        """xの属する集合と, yの属する集合を合併する

        Args:
            x (int): 集合の要素
            y (int): 集合の要素

        Note:
            Union By Rankで実装
        """
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def same_check(self, x: int, y: int) -> bool:
        """xとyが同じ集合に属しているかを判定

        Args:
            x (int): 集合に属する要素
            y (int): 集合に属する要素

        Returns:
            bool: 同じ集合に属するかどうか
        """
        return self.find(x) == self.find(y)

    def size(self, x: int) -> int:
        """xが属する集合の要素数を返す

        Args:
            x (int): 集合に属する要素

        Returns:
            int: xが属する集合の要素数
        """
        return -1 * self.parents[self.find(x)]
