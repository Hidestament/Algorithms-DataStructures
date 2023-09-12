# https://judge.yosupo.jp/submission/160823
# BinaryTrie Multi -> Singleにして高速化したもの

import sys
from typing import Optional


class BinaryTrie:
    def __init__(self, bit_size: int = 31):
        self.root = [None, None, 0]
        self.bit_size = bit_size

    def insert(self, x: int):
        """xを挿入する

        Args:
            x (int): 挿入する値

        TimeComplexity:
            O(bit_size)
        """
        digit = self.bit_size
        node = self.root
        node[-1] += 1
        while digit >= 0:
            bit = (x >> digit) & 1
            if node[bit] is None:
                node[bit] = [None, None, 0]

            # 部分木のサイズを更新
            node[bit][-1] += 1

            node = node[bit]
            digit -= 1

    def count(self, x: int) -> int:
        """xがいくつ含まれているかを返す

        Args:
            x (int): 検索する値

        Returns:
            int: 含まれている個数

        TimeComplexity:
            O(bit_size)
        """
        digit = self.bit_size
        node = self.root
        while digit >= 0:
            bit = (x >> digit) & 1
            if node[bit] is None:
                return 0

            node = node[bit]
            digit -= 1

        return node[-1]

    def discard(self, x: int):
        """xを1つ削除する

        Args:
            x (int): 削除する値

        Notes:
            xが存在しない場合は何もしない

        TimeComplexity:
            O(bit_size)
        """
        # 存在しない場合は何もしない
        if x not in self:
            return

        digit = self.bit_size
        node = self.root
        node[-1] -= 1
        while digit >= 0:
            bit = (x >> digit) & 1

            # 部分木のサイズを更新
            node[bit][-1] -= 1

            node = node[bit]
            digit -= 1

    def get_min_element_xor(self, x: int) -> Optional[int]:
        """xとxorが最小となる値を返す

        Args:
            x (int): xorする値

        Returns:
            Optional[int]: xとxorが最小となる値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) == 0:
            return None

        digit = self.bit_size
        min_element = 0

        node = self.root
        while digit >= 0:
            # x[digit] = 1 の場合, 右の子が最小
            if (x >> digit) & 1:
                if (node[1] is not None) and (node[1][-1] != 0):
                    node = node[1]
                    min_element |= 1 << digit
                else:
                    node = node[0]
            else:
                if (node[0] is not None) and (node[0][-1] != 0):
                    node = node[0]
                else:
                    node = node[1]
                    min_element |= 1 << digit

            digit -= 1

        return min_element

    def __len__(self) -> int:
        """要素数を返す

        Returns:
            int: 要素数
        """
        return self.root[2]

    def __contains__(self, x: int) -> bool:
        """xが含まれているかどうかを返す

        Args:
            x (int): 検索する値

        Returns:
            bool: xが含まれているかどうか

        TimeComplexity:
            O(bit_size)
        """
        return True if self.count(x) > 0 else False


input = sys.stdin.readline


tree = BinaryTrie(bit_size=30)
Q = int(input())

for _ in range(Q):
    q, x = list(map(int, input().split()))
    if q == 0:
        if x not in tree:
            tree.insert(x)
    elif q == 1:
        tree.discard(x)
    else:
        print(x ^ tree.get_min_element_xor(x))
