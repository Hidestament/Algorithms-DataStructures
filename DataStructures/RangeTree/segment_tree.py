from typing import Callable, Generic, TypeVar
from itertools import chain


T = TypeVar("T")


class SegmentTree(Generic[T]):
    """1点更新・区間集約Segment Tree.

    Attributes:
        _N (int): 元の配列のサイズ
        N (int): セグメント木の葉の数. N以上の最小の2のべき乗.
        data (list[T]): 元の配列の集約値を保存する木. 1-indexed.
        segfunc (Callable[[T, T], T]): モノイド上の2項演算.
        ide_ele (T): モノイド上の単位元.

    Methods:
        get(i: int): A[i], O(1).
        add(i: int, x: T): A[i] += x, O(logN).
        update(i: int, x: T): A[i] = x, O(logN).
        query(left: int, right: int): 非再帰segfunc(A[left..right)), O(logN).
        query_recursion(left: int, right: int): 再帰segfunc(A[left..right)), O(logN).

    Notes:
        Bit演算
        iの左の子 -> i << 1
        iの右の子 -> (i << 1) + 1
        iの親 -> i >> 1
    """

    def __init__(self, A: list[T], segfunc: Callable[[T, T], T], ide_ele: T):
        """1点更新・区間集約Segment Tree

        Args:
            A (list[T]): 元の配列
            segfunc (Callable[[T, T], T]): Segment Treeに乗せる演算
            ide_ele (T): segfuncに対する単位元

        TimeComplexity:
            O(N logN)
        """
        self._N = len(A)
        # N以上の最小の2のべき乗
        self.N = 1 << (self._N - 1).bit_length()
        self.segfunc = segfunc
        self.ide_ele = ide_ele

        # 配列の値
        self.data = self._build(A + [self.ide_ele] * (self.N - self._N))

    def _build(self, A: list[T]) -> list[T]:
        """元の配列からセグメント木を構築する

        Args:
            A (list[T]): 元の配列を2^kの長さに拡張した配列

        Returns:
            list[T]: Segment Tree
        """
        data = [A]
        for _ in range(self.N.bit_length() - 1):
            _A = data[-1]
            data.append([self.segfunc(_A[i], _A[i + 1]) for i in range(0, len(_A), 2)])

        data.append([self.ide_ele])
        return list(chain.from_iterable(data[::-1]))

    def __getitem__(self, i: int) -> T:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]
        """
        return self.get(i)

    def __setitem__(self, i: int, x: T):
        """A[i] = x

        Args:
            i (int): index. 0-indexed.
            x (T): update value.

        TimeComplexity:
            O(logN)
        """
        self.update(i, x)

    def get(self, i: int) -> T:
        """元の配列A[i]の値

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]
        """
        if not (0 <= i < self._N):
            raise IndexError("list index out of range")

        return self.data[i + self.N]

    def add(self, i: int, x: T):
        """A[i] += x

        Args:
            i (int): index. 0-indexed.
            x (T): add value.

        TimeComplexity:
            O(logN)
        """
        # i番目の葉の値から上に更新していく
        i += self.N
        self.data[i] += x
        while i > 1:
            # i //= 2 -> 親頂点
            i >>= 1
            self.data[i] = self.segfunc(self.data[i << 1], self.data[(i << 1) + 1])

    def update(self, i: int, x: T):
        """A[i] = x

        Args:
            i (int): index. 0-indexed.
            x (T): update value.

        TimeComplexity:
            O(logN)

        Note:
            ide_ele=float("inf")の場合, self.add()を使用すると挙動がおかしくなるため, こちらを使用する.
        """
        # i番目の葉の値から上に更新していく
        i += self.N
        self.data[i] = x
        while i > 1:
            # i //= 2 -> 親頂点
            i >>= 1
            self.data[i] = self.segfunc(self.data[i << 1], self.data[(i << 1) + 1])

    def _query_recursion(
        self,
        left: int,
        right: int,
        node_k: int,
        node_left: int,
        node_right: int,
    ) -> T:
        """A[left..right)を表すノードまで探索する

        Args:
            left (int): クエリ下限index. 0-indexed.
            right (int): クエリ上限index. 0-indexed.
            node_k (int): 現在見ているノード番号. 1-indexed.
            node_left (int): 現在見ているノードの左端index. 0-indexed.
            node_right (int): 現在見ているノードの右端index. 0-indexed.

        Returns:
            T: segfunc(A[left..right))
        """
        # 範囲外なら単位元を返す
        if (right <= node_left) or (node_right <= left):
            return self.ide_ele
        # ノード区間[node_left, node_right) ⊂ クエリ区間[left, right)
        # -> ノード区間の値を返す
        elif (left <= node_left) and (node_right <= right):
            return self.data[node_k]
        # クエリ区間[left, right) ⊂ ノード区間[node_left, node_right)
        # -> 左と右に分割
        else:
            left_value = self._query_recursion(
                left, right, node_k << 1, node_left, (node_left + node_right) >> 1
            )
            right_value = self._query_recursion(
                left,
                right,
                (node_k << 1) + 1,
                (node_left + node_right) >> 1,
                node_right,
            )
            return self.segfunc(left_value, right_value)

    def query_recursion(self, left: int, right: int) -> T:
        """再起segfunc(A[left..right))

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.

        Returns:
            T: segfunc(A[left..right))

        TimeComplexity:
            O(logN)
        """
        return self._query_recursion(left, right, 1, 0, self.N)

    def query(self, left: int, right: int) -> T:
        """非再起segfunc(A[left..right))

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.

        Returns:
            T: segfunc(A[left..right))

        TimeComplexity:
            O(logN)
        """
        # 葉から始める
        left += self.N
        right += self.N

        left_value = self.ide_ele
        right_value = self.ide_ele

        # ノードの値を集約できるのは, left -> 右の子, right -> 左の子のとき
        while left < right:
            # 奇数なら対象ノードは親の右のノードなので, 集約して一つ右のノードへ
            if left & 1:
                left_value = self.segfunc(left_value, self.data[left])
                left += 1

            # 奇数なら対象ノードは親の左のノードなので, 左に移動して集約
            if right & 1:
                right -= 1
                right_value = self.segfunc(self.data[right], right_value)

            # 親に登る
            left >>= 1
            right >>= 1

        return self.segfunc(left_value, right_value)


def RangeMinimumQuery(A: list[int]) -> SegmentTree[int]:
    """Range Minimum Query

    Args:
        A (list[int]): Segment Treeに乗せる配列

    Returns:
        SegmentTree[int]: Range Minimum Query
    """
    return SegmentTree[int](A, min, 10**15)


def RangeSumQuery(A: list[int]) -> SegmentTree[int]:
    """Range Sum Query

    Args:
        A (list[int]): Segment Treeに乗せる配列

    Returns:
        SegmentTree[int]: Range Sum Query
    """
    return SegmentTree[int](A, lambda x, y: x + y, 0)


def RangeCompositeQuery(A: list[list[int, int]]) -> SegmentTree[list[list[int, int]]]:
    """Range Composite Query

    Args:
        A (list[list[int, int]]): Segment Treeに乗せる配列

    Returns:
        SegmentTree[list[list[int, int]]]: Range Composite Query

    Notes:
        A[i] = [a, b] -> f_i(x) = ax + b
        query(left, right) = f_{right-1}(f_{right-2}..(...f_{left}(x)))
        MOD付き
    """
    MOD = 998244353
    return SegmentTree[list[list[int, int]]](
        A=A,
        segfunc=lambda x, y: [(y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD],
        ide_ele=[1, 0],
    )
