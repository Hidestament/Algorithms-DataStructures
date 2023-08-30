from typing import Optional
from itertools import accumulate

from DataStructures.BitVector.bit_vector_base import BitVectorBase


class BitVectorAcc(BitVectorBase):
    """0-1の配列Bに対して, 累積和を使用したビットベクトル

    Methods:
        - rank0(i): B[0..i)の0の個数. O(1).
        - rank1(i): B[0..i)の1の個数. O(1).
        - rank0_all(): Bの0の個数. O(1).
        - rank1_all(): Bの1の個数. O(1).
        - select0(k): 0がk番目に現れるindex. O(logN)
        - select1(k): 1がk番目に現れるindex. O(logN)
    """
    def __init__(self, B: list[int]):
        """累積和を使用したビットベクトル

        Args:
            B (list[int]): 要素は0 or 1
        """
        self.B = B
        self.acc = list(accumulate(B))

    def __len__(self) -> int:
        """元の配列の長さ

        Returns:
            int: 元の配列の長さ
        """
        return len(self.B)

    def __getitem__(self, i: int) -> int:
        """B[i]を取得

        Args:
            i (int): i番目の要素

        Returns:
            int: B[i]
        """
        return self.B[i]

    def rank0(self, i: int) -> int:
        """元の配列B[0..i)の0の個数

        Args:
            i (int): 上限 (含まない).

        Returns:
            int: 0の個数

        TimeComplexity:
            O(1)
        """
        if i <= 0:
            return 0
        i = min(i, len(self))
        return i - self.rank1(i)

    def rank1(self, i: int) -> int:
        """元の配列B[0..i)の1の個数

        Args:
            i (int): 上限 (含まない).

        Returns:
            int: 1の個数

        TimeComplexity:
            O(1)
        """
        if i <= 0:
            return 0
        i = min(i, len(self))
        return self.acc[i - 1]

    def rank0_all(self) -> int:
        """元の配列Bの0の個数

        Returns:
            int: 0の個数

        TimeComplexity:
            O(1)
        """
        return self.rank0(len(self.B))

    def rank1_all(self) -> int:
        """元の配列Bの1の個数

        Returns:
            int: 1の個数

        TimeComplexity:
            O(1)
        """
        return self.rank1(len(self.B))

    def select0(self, k: int) -> Optional[int]:
        """0がk番目に現れるindexを返す

        Args:
            k (int): k番目. 1-indexed.

        Returns:
            Optional[int]: 該当のindex. 存在しない場合はNone

        TimeComplexity:
            O(log N)
        """
        if (k <= 0) or (k > self.rank0_all()):
            return None

        left, right = 0, len(self)
        while (right - left) > 1:
            mid = (left + right) // 2
            if self.rank0(mid) < k:
                left = mid
            else:
                right = mid
        return left

    def select1(self, k: int) -> Optional[int]:
        """1がk番目に現れるindexを返す

        Args:
            k (int): k番目. 1-indexed.

        Returns:
            Optional[int]: 該当のindex. 存在しない場合はNone

        TimeComplexity:
            O(log N)
        """
        if (k <= 0) or (k > self.rank1_all()):
            return None

        left, right = 0, len(self)
        while (right - left) > 1:
            mid = (left + right) // 2
            if self.rank1(mid) < k:
                left = mid
            else:
                right = mid
        return left
