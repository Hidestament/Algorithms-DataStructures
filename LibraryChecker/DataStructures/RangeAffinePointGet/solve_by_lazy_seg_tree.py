# https://judge.yosupo.jp/submission/159426
# LazySegmentTreeを高速化したもの

from array import array
import sys

MOD = 998244353


class LazySegmentTree:
    """抽象化LazySegmentTreeを高速化したもの

    Attributes:
        _N: 元の配列の長さ
        N: segment tree用に拡張した配列の長さ, _N以上の最小の2のべき乗
        data (list[int]): データを格納するSegment Tree. 1-indexedで扱う.
        lazy (list[tuple[int, int]]): 遅延配列

    Methods:
        range_update(left: int, right: int, x: list[int, int]): A[left..right)の値をrange_update_func(x)で更新する, O(logN)
        get(i: int): A[i], O(logN)

    Notes:
        Bit演算
        iの左の子 -> i << 1
        iの右の子 -> (i << 1) + 1
        iの親 -> i >> 1
        i & -i ->
    """

    def __init__(self, A: list[int]):
        """Segment Tree

        Args:
            A (list[T]): 元の配列

        TimeComplexity:
            O(N logN)
        """
        self._N = len(A)
        # N以上の最小の2のべき乗
        self.N = 1 << (self._N - 1).bit_length()

        # 配列の値
        self.data = array("i", [0] * (2 * self.N))
        for i, a in enumerate(A, start=self.N):
            self.data[i] = a
        # 遅延配列
        self.lazy: list[list[int, int]] = [(1, 0)] * (2 * self.N)

    def _propagate(self, node_k: int):
        """ノードnode_kの遅延情報を子に伝播し, ノードnode_kの値を更新する

        Args:
            k (int): segment treeのノード番号. 1-indexed.
        """
        # 葉でない場合 -> 子に伝播 & 値の更新
        if node_k < self.N:
            self.lazy[node_k << 1] = (
                (self.lazy[node_k][0] * self.lazy[node_k << 1][0]) % MOD,
                (self.lazy[node_k][0] * self.lazy[node_k << 1][1] + self.lazy[node_k][1]) % MOD,
            )
            self.lazy[(node_k << 1) + 1] = (
                (self.lazy[node_k][0] * self.lazy[(node_k << 1) + 1][0]) % MOD,
                (self.lazy[node_k][0] * self.lazy[(node_k << 1) + 1][1] + self.lazy[node_k][1]) % MOD,
            )

        if self.N <= node_k:
            self.data[node_k] = (self.lazy[node_k][0] * self.data[node_k] + self.lazy[node_k][1]) % MOD
        self.lazy[node_k] = (1, 0)

    def _propagated_segment(self, left: int, right: int) -> list[int]:
        """A[left..right)を表すノードのうち, 遅延情報を先に伝播すべきノードを返す

        Args:
            left (int): 下限, 0-indexed.
            right (int): 上限, 0-indexed.

        Returns:
            list[int]: 遅延情報を先に伝播すべきノードを返す
        """
        # 葉からスタート
        left += self.N
        right += self.N

        # スキップして良い区間 (trailing zerosを取り除いた区間まで)
        skip_left = left >> ((left & -left).bit_length())
        skip_right = right >> ((right & -right).bit_length())

        segment = []
        while (left < right) and (left > 0):
            # Rightから更新
            if right <= skip_right:
                segment.append(right)

            if left <= skip_left:
                segment.append(left)
            left >>= 1
            right >>= 1

        while left:
            segment.append(left)
            left >>= 1

        return segment[::-1]

    def range_update(self, left: int, right: int, x: list[int, int]):
        """非再帰 A[left..right)の値をrange_update_func(x)で上書きする

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.
            x (list[int, int]): 更新値.

        Notes
            1. 根 -> 対象区間までLazyを伝播
            2. 対象区間を処理
            3. 対象区間 -> 根までDataの値を更新

        TimeComplexity:
            O(log N)
        """
        propagated_segment = self._propagated_segment(left, right)

        # 1. 根 -> 対象区間までLazyを伝播
        for node_k in propagated_segment:
            self._propagate(node_k)

        # 2. 対象区間の更新
        left += self.N
        right += self.N
        length = 1
        while left < right:
            self._propagate(left)
            self._propagate(right - 1)

            # 奇数なら対象ノードは親の右のノードなので, 対象区間
            if left & 1:
                self.lazy[left] = x
                self._propagate(left)
                left += 1

            # 奇数なら対象ノードは親の左のノードなので, 対象区間
            if right & 1:
                right -= 1
                self.lazy[right] = x
                self._propagate(right)

            # 親に登る
            left >>= 1
            right >>= 1
            length <<= 1

    def get(self, i: int) -> int:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            T: A[i]

        TimeComplexity:
            O(log N)
        """
        node_k = 1
        node_left, node_right = 0, self.N
        while node_k < len(self.data):
            self._propagate(node_k)

            node_mid = (node_left + node_right) >> 1
            # 左の子に含まれる場合
            if i < node_mid:
                node_k <<= 1
                node_right = node_mid
            # 右の子に含まれる場合
            else:
                node_k = (node_k << 1) + 1
                node_left = node_mid

        return self.data[i + self.N]


input = sys.stdin.readline


N, Q = map(int, input().split())
A = list(map(int, input().split()))

seg = LazySegmentTree(A)

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        left, right, b, c = query[1:]
        seg.range_update(left, right, [b, c])
    else:
        i = query[1]
        print(seg.get(i) % MOD)
