from abc import ABCMeta, abstractmethod
from typing import Optional


class BitVectorBase(metaclass=ABCMeta):
    @abstractmethod
    def __getitem__(self, i: int) -> int:
        """B[i]を取得

        Args:
            i (int): i番目の要素

        Returns:
            int: B[i]
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """元の配列の長さ

        Returns:
            int: 元の配列の長さ
        """
        pass

    @abstractmethod
    def rank0(self, i: int) -> int:
        """元の配列B[0..i)の0の個数

        Args:
            i (int): 上限

        Returns:
            int: 0の個数

        Note:
            O(1) or O(log N)で実装する
        """
        pass

    @abstractmethod
    def rank1(self, i: int) -> int:
        """元の配列B[0..i)の1の個数

        Args:
            i (int): 上限

        Returns:
            int: 1の個数

        Note:
            O(1) or O(log N)で実装する
        """
        pass

    @abstractmethod
    def rank0_all(self) -> int:
        """元の配列Bの0の個数

        Returns:
            int: 0の個数

        Note:
            O(1) or O(log N)で実装する
        """
        pass

    @abstractmethod
    def rank1_all(self) -> int:
        """元の配列Bの1の個数

        Returns:
            int: 1の個数

        Note:
            O(1) or O(log N)で実装する
        """
        pass

    @abstractmethod
    def select0(self, k: int) -> Optional[int]:
        """0がk番目に現れるindexを返す

        Args:
            k (int): k番目. 1-indexed.

        Returns:
            Optional[int]: 該当のindex. 存在しない場合はNone

        Note:
            O(1) or O(log N)で実装する
        """
        pass

    @abstractmethod
    def select1(self, k: int) -> Optional[int]:
        """1がk番目に現れるindexを返す

        Args:
            k (int): k番目. 1-indexed.

        Returns:
            Optional[int]: 該当のindex. 存在しない場合はNone

        Note:
            O(1) or O(log N)で実装する
        """
        pass
