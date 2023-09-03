from typing import Optional, Callable, TypeVar, Generic
from itertools import chain


T = TypeVar("T")


class LazySegmentTree(Generic[T]):
    """区間更新・区間取得を O(log N)で行う

    Attributes:
        _N: 元の配列の長さ
        N: segment tree用に拡張した配列の長さ, _N以上の最小の2のべき乗
        segfunc (Callable[[T, T], T]): Segment Treeに乗せる演算
        ide_ele (T): segfuncに対する単位元
        lazy_propagator (Callable[[T, Optional[T]], T]): 遅延情報を子に伝播する関数
        lazy_calculator (Callable[[Optional[T], int, int, T], T]): 遅延情報を更新する関数
        range_update_func (Callable[[T, T], T]): 遅延情報を元の配列に反映する関数
        data (list[T]): データを格納するSegment Tree. 1-indexedで扱う.
        lazy (list[Optional[T]]): 遅延配列

    Methods:
        range_update_recursion(left: int, right: int, x: T): A[left..right)の値をrange_update_func(x)で更新する, O(logN)
        one_point_update_recursion(i: int, x: T): A[i..i+1)の値をrange_update_func(x)で更新する, O(logN)
        query_recursion(left: int, right: int): segfunc(A[left..right))の値を取得する, O(logN)
        get(i: int): A[i], O(logN)

    Notes:
        Bit演算
        iの左の子 -> i << 1
        iの右の子 -> (i << 1) + 1
        iの親 -> i >> 1
    """

    def __init__(
        self,
        A: list[T],
        segfunc: Callable[[T, T], T],
        ide_ele: T,
        lazy_propagator: Callable[[T, Optional[T]], T],
        lazy_calculator: Callable[[Optional[T], int, int, T], T],
        range_update_func: Callable[[T, T], T],
    ):
        """Segment Tree

        Args:
            A (list[T]): 元の配列
            segfunc (Callable[[T, T], T]): Segment Treeに乗せる演算
            ide_ele (T): segfuncに対する単位元
            lazy_propagator (Callable[[T, Optional[T]], T]): 遅延情報を子に伝播する関数
            lazy_calculator (Callable[[Optional[T], int, int, T], T]): 遅延情報を更新する関数
            range_update_func (Callable[[T, T], T]): 遅延情報を元の配列に反映する関数

        TimeComplexity:
            O(N logN)
        """
        self._N = len(A)
        # N以上の最小の2のべき乗
        self.N = 1 << (self._N - 1).bit_length()
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.lazy_propagator = lazy_propagator
        self.lazy_calculator = lazy_calculator
        self.range_update_func = range_update_func

        # 配列の値
        self.data = self._build(A + [self.ide_ele] * (self.N - self._N))
        # 遅延配列
        self.lazy: list[Optional[T]] = [None] * (2 * self.N)

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

    def _propagate(self, node_k: int):
        """ノードnode_kの遅延情報を子に伝播し, ノードnode_kの値を更新する

        Args:
            k (int): segment treeのノード番号. 1-indexed.
        """
        # 伝播する値がない場合 -> 何もしない
        if self.lazy[node_k] is None:
            return

        # 葉でない場合 -> 子に伝播 & 値の更新
        if node_k < self.N:
            self.lazy[node_k << 1] = self.lazy_propagator(
                self.lazy[node_k], self.lazy[node_k << 1]
            )
            self.lazy[(node_k << 1) + 1] = self.lazy_propagator(
                self.lazy[node_k], self.lazy[(node_k << 1) + 1]
            )

        self.data[node_k] = self.range_update_func(self.data[node_k], self.lazy[node_k])
        self.lazy[node_k] = None

    def _range_update_recursion(
        self,
        left: int,
        right: int,
        x: T,
        node_k: int,
        node_left: int,
        node_right: int,
    ):
        """A[left..right)を表すノードまで探索し, その過程で遅延情報, ノードの値を更新する

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.
            x (T): 更新値.
            node_k (int): 現在見ているノード番号. 1-indexed.
            node_left (int): 現在見ているノードの左端index. 0-indexed.
            node_right (int): 現在見ているノードの右端index. 0-indexed.
        """
        # 最初に既に存在する遅延情報を処理する
        self._propagate(node_k)

        # 範囲外 -> 何もしない
        if (right <= node_left) or (node_right <= left):
            return
        # ノード区間[node_left, node_right) ⊂ クエリ区間[left, right) -> 遅延情報を更新
        elif (left <= node_left) and (node_right <= right):
            self.lazy[node_k] = self.lazy_calculator(
                self.lazy[node_k], node_left, node_right, x
            )
            self._propagate(node_k)
        # クエリ区間[left, right) ⊂ ノード区間[node_left, node_right) -> 左と右に分割
        else:
            left_node_k, right_node_k = node_k << 1, (node_k << 1) + 1
            self._range_update_recursion(
                left, right, x, left_node_k, node_left, (node_left + node_right) >> 1
            )
            self._range_update_recursion(
                left, right, x, right_node_k, (node_left + node_right) >> 1, node_right
            )
            self.data[node_k] = self.segfunc(
                self.data[left_node_k], self.data[right_node_k]
            )

    def range_update_recursion(self, left: int, right: int, x: T):
        """A[left..right)の値をrange_update_func(x)で上書きする

        Args:
            left (int): 下限index. 0-indexed.
            right (int): 上限index. 0-indexed.
            x (T): 更新値.

        TimeComplexity:
            O(log N)
        """
        self._range_update_recursion(left, right, x, 1, 0, self.N)

    def one_point_update_recursion(self, i: int, x: T):
        """1点更新 A[i] = range_update_func(x)

        Args:
            i (int): index, 0-indexed
            x (T): 更新値
        """
        self.range_update_recursion(i, i + 1, x)

    def _query_recursion(
        self,
        left: int,
        right: int,
        node_k: int,
        node_left: int,
        node_right: int,
    ) -> T:
        """A[left..right)を表すノードまで探索し値を返す. その過程で遅延情報, ノードの値を更新する

        Args:
            left (int): クエリ下限index. 0-indexed.
            right (int): クエリ上限index. 0-indexed.
            node_k (int): 現在見ているノード番号. 1-indexed.
            node_left (int): 現在見ているノードの左端index. 0-indexed.
            node_right (int): 現在見ているノードの右端index. 0-indexed.

        Returns:
            T: segfunc(A[left..right))
        """
        # 遅延情報の処理
        self._propagate(node_k)

        # 範囲外 -> 単位元
        if (right <= node_left) or (node_right <= left):
            return self.ide_ele
        # ノード区間[node_left, node_right) ⊂ クエリ区間[left, right) -> ノード区間の値
        elif (left <= node_left) and (node_right <= right):
            return self.data[node_k]
        # クエリ区間[left, right) ⊂ ノード区間[node_left, node_right) -> 左右の子へ再帰的に探索
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

    def __getitem__(self, i: int) -> T:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            T: A[i]

        TimeComplexity:
            O(logN)
        """
        return self.get(i)

    def get(self, i: int) -> T:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            T: A[i]

        TimeComplexity:
            O(log N)
        """
        if not (0 <= i < self._N):
            raise IndexError("list index out of range")

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


def RangeMinimumRangeAdd(A: list[int]) -> LazySegmentTree[int]:
    """Range Minimum Query & Range Add Query

    Args:
        A (list[int]): Segment Treeに乗せる元の配列

    Returns:
        LazySegmentTree: Range Minimum Query & Range Add Query
    """

    def range_update_func(original_value: int, updated_value: int) -> int:
        return original_value + updated_value

    def lazy_calculator(
        lazy_value: Optional[int], node_left: int, node_right: int, x: int
    ) -> int:
        if lazy_value is None:
            return x
        return lazy_value + x

    def lazy_propagator(parent_value: int, child_value: Optional[int]) -> int:
        if child_value is None:
            return parent_value
        return parent_value + child_value

    return LazySegmentTree[int](
        A, min, 10**15, lazy_propagator, lazy_calculator, range_update_func
    )


def RangeMinimumRangeUpdate(A: list[int]) -> LazySegmentTree[int]:
    """Range Minimum Query & Range Update Query

    Args:
        A (list[int]): Segment Treeに乗せる元の配列

    Returns:
        LazySegmentTree: Range Minimum Query & Range Update Query
    """

    def range_update_func(original_value: int, updated_value: int) -> int:
        return updated_value

    def lazy_calculator(
        lazy_value: Optional[int], node_left: int, node_right: int, x: int
    ) -> int:
        return x

    def lazy_propagator(parent_value: int, child_value: Optional[int]) -> int:
        return parent_value

    return LazySegmentTree[int](
        A, min, 10**15, lazy_propagator, lazy_calculator, range_update_func
    )


def RangeSumRangeAdd(A: list[int]) -> LazySegmentTree[int]:
    """Range Sum Query & Range Add Query

    Args:
        A (list[int]): Segment Treeに乗せる元の配列

    Returns:
        LazySegmentTree: Range Sum Query & Range Add Query
    """

    def range_update_func(original_value: int, updated_value: int) -> int:
        return original_value + updated_value

    def lazy_calculator(
        lazy_value: Optional[int], node_left: int, node_right: int, x: int
    ) -> int:
        added_value = (node_right - node_left) * x
        if lazy_value is None:
            return added_value
        return lazy_value + added_value

    def lazy_propagator(parent_value: int, child_value: Optional[int]) -> int:
        if child_value is None:
            return parent_value >> 1
        return (parent_value >> 1) + child_value

    return LazySegmentTree[int](
        A, lambda x, y: x + y, 0, lazy_propagator, lazy_calculator, range_update_func
    )


def RangeSumRangeUpdate(A: list[int]) -> LazySegmentTree[int]:
    """Range Sum Query & Range Update Query

    Args:
        A (list[int]): Segment Treeに乗せる元の配列

    Returns:
        LazySegmentTree: Range Sum Query & Range Update Query
    """

    def range_update_func(original_value: int, updated_value: int) -> int:
        return updated_value

    def lazy_calculator(
        lazy_value: Optional[int], node_left: int, node_right: int, x: int
    ) -> int:
        return (node_right - node_left) * x

    def lazy_propagator(parent_value: int, child_value: Optional[int]) -> int:
        return parent_value >> 1

    return LazySegmentTree[int](
        A, lambda x, y: x + y, 0, lazy_propagator, lazy_calculator, range_update_func
    )
