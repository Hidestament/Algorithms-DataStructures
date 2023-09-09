from typing import Optional
from array import array


class BinaryIndexedTree:
    """部分和 + 一点更新を O(log N)で行う

    Attributes:
        size (int): 配列の要素数
        data (list[int]): データを格納するBinary Indexed Tree. 1-indexedで扱う.

    Methods:
        get(i): A[i], O(logN)
        add(i, x): A[i] += x, O(logN)
        update(i, x): A[i] = x, O(logN)
        sum(i): sum(A[0..i)), O(logN)
        sum_range(i, j): sum(A[i..j)), O(logN)
        lower_bound(x): A[0] + A[1] + ... A[i - 1] >= x となる最小のi, O(logN)

    Notes:
        - 0-indexedで扱う (内部では1-indexedで扱う)
    """

    def __init__(self, A: list[int]):
        """Binary Indexed Tree

        Args:
            A (list[int]): 元の配列
        """
        self.size = len(A) + 1
        self.data = array("q", [0] * self.size)

        for i, a in enumerate(A):
            self.update(i, a)

    def __getitem__(self, i: int) -> int:
        """A[i]を取得.

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]

        TimeComplexity:
            O(log N)
        """
        return self.get(i)

    def get(self, i: int) -> int:
        """A[i]を取得.

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: A[i]

        TimeComplexity:
            O(log N)
        """
        if not (0 <= i < self.size):
            raise IndexError("list index out of range")

        return self.sum(i + 1) - self.sum(i)

    def add(self, i: int, x: int):
        """A[i] += x

        Args:
            i (int): index. 0-indexed.
            x (int): 加算する値.

        TimeComplexity:
            O(log N)
        """
        if i < 0:
            return

        i += 1
        while i < self.size:
            self.data[i] += x
            # 真上の位置は, iにiのLSBを加えたモノ
            i += i & -i

    def update(self, i: int, x: int):
        """A[i] = xに更新する

        Args:
            i (int): index. 0-indexed.
            x (int): 更新値.

        TimeComplexity:
            O(log N)
        """
        if i < 0:
            return

        self.add(i, -self.get(i) + x)

    def sum(self, i: int) -> int:
        """A[0..i)の総和

        Args:
            i (int): index. 0-indexed.

        Returns:
            int: sum(A[:i])

        TimeComplexity:
            O(log N)
        """
        if i <= 0:
            return 0

        i = min(i, self.size - 1)
        s = 0
        while i > 0:
            s += self.data[i]
            i -= i & -i

        return s

    def sum_range(self, i: int, j: int) -> int:
        """A[i..j)の総和

        Args:
            i (int): index. 0-indexed.
            j (int): index. 0-indexed.

        Returns:
            int: sum(A[i:j])

        TimeComplexity:
            O(log N)
        """
        if i >= j:
            return 0
        return self.sum(j) - self.sum(i)

    def lower_bound(self, x: int) -> Optional[int]:
        """A[0] + A[1] + ... A[i - 1] >= x となる最小のiを取得

        Args:
            x (int): lower bound.

        Returns:
            Optional[int]: index. 0-indexed. 含まない. 該当するものがない場合はNone.

        TimeComplexity:
            O(log N)

        Note:
            各項は非負である必要がある
        """
        if x <= 0:
            return 0

        if self.sum(self.size) < x:
            return None

        # 現在見ている区間の範囲
        length = self.size
        s = 0
        i = 0
        while length > 0:
            # 現在の区間を足してもxに届かない場合, その区間を加えて右の子へ
            if (i + length < self.size) and self.data[i + length] + s < x:
                s += self.data[i + length]
                i += length

            # 1つ下の階層へ (区間は半分になる)
            length //= 2

        return i + 1
