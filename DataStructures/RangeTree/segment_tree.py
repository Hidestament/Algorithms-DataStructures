from typing import Callable


class SegmentTree:
    """1点更新・区間集約Segment Tree. 非再起, 0-index, 非可換.

    Method:
        - get(i): A[i]を取得 O(1).
        - add(i, x): A[i] += x O(logN).
        - update(i, x): A[i] = x O(logN).
        - query(left, right): segfunc(A[left..right)) O(logN).

    Notes:
        i番目のノードの
        - 左の子: i * 2 = i << 1
        - 右の子: i * 2 + 1 = (i << 1) + 1
        - 親: i // 2 = i >> 1
    """

    def __init__(self, N: int, segfunc: Callable, ide_ele: int):
        """1点更新・区間集約Segment Tree

        Args:
            N (int): 元の配列のサイズ
            segfunc (Callable): モノイド上の2項演算.
            ide_ele (int): モノイド上の単位元.

        Notes:
            - 0-indexed (内部では1-indexed)
            - 非再帰

        TimeComplexity:
            O(N)
        """
        self._N = N
        # N以上の最小の2のべき乗
        self.N = 1 << (N - 1).bit_length()
        self.tree = [ide_ele] * (2 * self.N)
        self.segfunc = segfunc
        self.ide_ele = ide_ele

    def __getitem__(self, i: int) -> int:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]
        """
        return self.get(i)

    def get(self, i: int) -> int:
        """元の配列A[i]の値を取得する

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]
        """
        if not (0 <= i < self._N):
            raise IndexError("list index out of range")

        return self.tree[i + self.N]

    def add(self, i: int, x: int):
        """A[i] += xとする

        Args:
            i (int): index. 0-indexed.
            x (int): update value.

        TimeComplexity:
            O(logN)
        """
        # i番目の葉の値から上に更新していく
        i += self.N
        self.tree[i] += x
        while i > 1:
            # i //= 2 -> 親頂点
            i >>= 1
            self.tree[i] = self.segfunc(
                self.tree[i << 1], self.tree[(i << 1) + 1]
            )

    def update(self, i: int, x: int):
        """A[i] = x とする

        Args:
            i (int): index. 0-indexed.
            x (int): update value.

        TimeComplexity:
            O(logN)

        Note:
            ide_ele=float("inf")の場合, self.add()を使用すると挙動がおかしくなるため, こちらを使用する.
        """
        # i番目の葉の値から上に更新していく
        i += self.N
        self.tree[i] = x
        while i > 1:
            # i //= 2 -> 親頂点
            i >>= 1
            self.tree[i] = self.segfunc(
                self.tree[i << 1], self.tree[(i << 1) + 1]
            )

    def _query_recursion(
        self,
        left: int,
        right: int,
        node: int,
        node_left: int,
        node_right: int,
    ) -> int:
        """クエリ区間[left, right)に対する再帰関数

        Args:
            left (int): クエリ下限index. 0-indexed. A[left]は含む.
            right (int): クエリ上限index. 0-indexed. A[right]は含まない.
            node (int): 現在見ているノード番号. 1-indexed.
            node_left (int): 現在見ているノードの左端index. 0-indexed.
            node_right (int): 現在見ているノードの右端index. 0-indexed.

        Returns:
            int: segfunc(A[left..right))
        """
        # 範囲外なら単位元を返す
        if (right <= node_left) or (node_right <= left):
            return self.ide_ele

        # ノード区間[node_left, node_right) ⊂ クエリ区間[left, right)
        # ノード区間の値を返す
        elif (left <= node_left) and (node_right <= right):
            return self.tree[node]

        # クエリ区間[left, right) ⊂ ノード区間[node_left, node_right)
        # 左と右に分割
        else:
            left_value = self._query_recursion(left, right, node << 1, node_left, (node_left + node_right) >> 1)
            right_value = self._query_recursion(left, right, (node << 1) + 1, (node_left + node_right) >> 1, node_right)
            return self.segfunc(left_value, right_value)

    def query_recursion(self, left: int, right: int) -> int:
        """再起segfunc(A[left..right))を求める. A[right]は含まない

        Args:
            left (int): 下限index. 0-indexed. A[left]は含む.
            right (int): 上限index. 0-indexed. A[right]は含まない.

        Returns:
            int: segfunc(A[left..right))

        TimeComplexity:
            O(logN)
        """
        return self._query_recursion(left, right, 1, 0, self.N)

    def query(self, left: int, right: int) -> int:
        """非再起segfunc(A[left..right))を求める. A[right]は含まない

        Args:
            left (int): 下限index. 0-indexed. A[left]は含む.
            right (int): 上限index. 0-indexed. A[right]は含まない.

        Returns:
            int: segfunc(A[left..right))

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
                left_value = self.segfunc(left_value, self.tree[left])
                left += 1

            # 奇数なら対象ノードは親の左のノードなので, 左に移動して集約
            if right & 1:
                right -= 1
                right_value = self.segfunc(self.tree[right], right_value)

            # 親に登る
            left >>= 1
            right >>= 1

        return self.segfunc(left_value, right_value)
