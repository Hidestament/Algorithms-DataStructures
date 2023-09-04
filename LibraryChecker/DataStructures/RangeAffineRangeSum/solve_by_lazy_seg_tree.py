# https://judge.yosupo.jp/submission/159438
# 抽象化LazySegmentTreeを高速化したもの

from itertools import chain
import sys
from array import array


MOD = 998244353
INV_2 = pow(2, -1, MOD)


class LazySegmentTree:
    """区間更新・区間取得を O(log N)で行う

    Attributes:
        _N: 元の配列の長さ
        N: segment tree用に拡張した配列の長さ, _N以上の最小の2のべき乗
        data (list[int]): データを格納するSegment Tree. 1-indexedで扱う.
        lazy (list[tuple[int, int]]): 遅延配列

    Methods:
        range_update(left: int, right: int, x: tuple[int, int]): 非再帰 A[left..right)の値をrange_update_func(x)で更新する, O(logN)
        query(left: int, right: int): 非再帰 sum(A[left..right))の値を取得する, O(logN)
    """

    def __init__(self, A: list[int]):
        """Segment Tree

        Args:
            A (list[int]): 元の配列

        TimeComplexity:
            O(N logN)
        """
        self._N = len(A)
        # N以上の最小の2のべき乗
        self.N = 1 << (self._N - 1).bit_length()

        # 配列の値
        self.data = self._build(A + [0] * (self.N - self._N))
        # 遅延配列
        self.lazy: list[tuple[int, int]] = [(1, 0) for _ in range(2 * self.N)]

    def _build(self, A: list[int]) -> list[int]:
        """元の配列からセグメント木を構築する

        Args:
            A (list[int]): 元の配列を2^kの長さに拡張した配列

        Returns:
            list[int]: Segment Tree
        """
        data = [A]
        for _ in range(self.N.bit_length() - 1):
            _A = data[-1]
            data.append([(_A[i] + _A[i + 1]) % MOD for i in range(0, len(_A), 2)])

        data.append([0])
        return array("i", chain.from_iterable(data[::-1]))

    def _propagate(self, node_k: int):
        """ノードnode_kの遅延情報を子に伝播し, ノードnode_kの値を更新する

        Args:
            k (int): segment treeのノード番号. 1-indexed.
        """
        # 伝播する値がない場合 -> 何もしない
        if self.lazy[node_k] == (1, 0):
            return

        # 葉でない場合 -> 子に伝播 & 値の更新
        if node_k < self.N:
            self.lazy[node_k << 1] = (
                (self.lazy[node_k][0] * self.lazy[node_k << 1][0]) % MOD,
                (
                    self.lazy[node_k][1] * INV_2
                    + self.lazy[node_k][0] * self.lazy[node_k << 1][1]
                )
                % MOD,
            )
            self.lazy[(node_k << 1) + 1] = (
                (self.lazy[node_k][0] * self.lazy[(node_k << 1) + 1][0]) % MOD,
                (
                    self.lazy[node_k][1] * INV_2
                    + self.lazy[node_k][0] * self.lazy[(node_k << 1) + 1][1]
                )
                % MOD,
            )

        self.data[node_k] = (
            self.lazy[node_k][0] * self.data[node_k] + self.lazy[node_k][1]
        ) % MOD
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

    def range_update(self, left: int, right: int, x: tuple[int, int]):
        """非再帰 A[left..right)の値をrange_update_func(x)で上書きする

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.
            x (tuple[int, int]): 更新値.

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
                self.lazy[left] = (x[0], (length * x[1]) % MOD)
                self._propagate(left)
                left += 1

            # 奇数なら対象ノードは親の左のノードなので, 対象区間
            if right & 1:
                right -= 1
                self.lazy[right] = (x[0], (length * x[1]) % MOD)
                self._propagate(right)

            # 親に登る
            left >>= 1
            right >>= 1
            length <<= 1

        # 3. 対象区間 -> 根までのDataの値を更新
        for node_k in reversed(propagated_segment):
            self._propagate(node_k << 1)
            self._propagate((node_k << 1) + 1)
            self.data[node_k] = (
                self.data[node_k << 1] + self.data[(node_k << 1) + 1]
            ) % MOD

    def query(self, left: int, right: int) -> int:
        """非再起segfunc(A[left..right))

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.

        Returns:
            T: segfunc(A[left..right))

        Notes
            1. 根 -> 対象区間までLazyを伝播
            2. 対象区間の集約値を計算

        TimeComplexity:
            O(logN)
        """
        propagated_segment = self._propagated_segment(left, right)

        # 1. 根 -> 対象区間までLazyを伝播
        for node_k in propagated_segment:
            self._propagate(node_k)

        # 2. 対象区間の集約地の取得
        left += self.N
        right += self.N

        s = 0
        while left < right:
            # 奇数なら対象ノードは親の右のノードなので, 対象区間
            if left & 1:
                self._propagate(left)
                s += self.data[left]
                s %= MOD
                left += 1

            # 奇数なら対象ノードは親の左のノードなので, 対象区間
            if right & 1:
                right -= 1
                self._propagate(right)
                s += self.data[right]
                s %= MOD

            # 親に登る
            left >>= 1
            right >>= 1

        return s % MOD


if __name__ == "__main__":
    input = sys.stdin.readline

    MOD = 998244353

    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    seg = LazySegmentTree(A)
    for _ in range(Q):
        query = list(map(int, input().split()))
        if query[0] == 0:
            left, right, b, c = query[1:]
            seg.range_update(left, right, (b, c))
        else:
            left, right = query[1:]
            print(seg.query(left, right) % MOD)
