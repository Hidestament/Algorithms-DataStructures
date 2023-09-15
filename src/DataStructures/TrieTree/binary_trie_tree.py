from typing import Optional


class BinaryTrie:
    """非負整数を扱うTrie木, 多重集合のように使え, xor系のクエリに強い

    Attributes:
        root (list): トライ木の根
        bit_size (int): ビット数

    Methods:
        insert(x): xを挿入する, O(bit_size)
        count(x): xがいくつ含まれているかを返す, O(bit_size)
        discard(x): xを1つ削除する, O(bit_size)
        get_min_element(): 最小値を返す, O(bit_size)
        get_max_element(): 最大値を返す, O(bit_size)
        get_min_element_xor(x): xとxorが最小となる値を返す, O(bit_size)
        get_max_element_xor(x): xとxorが最大となる値を返す, O(bit_size)
        get_kth_smallest_element(k): k番目に小さい値を返す, O(bit_size)
        get_kth_largest_element(k): k番目に大きい値を返す, O(bit_size)
        pop_min_element(): 最小値を削除して返す, O(bit_size)
        pop_max_element(): 最大値を削除して返す, O(bit_size)
    """

    def __init__(self, bit_size: int = 31):
        self.root = self._new_node()
        self.bit_size = bit_size

    def _new_node(self) -> list:
        """新しいノードを作成する

        Returns:
            list: [左の子(bit 0), 右の子(bit 1), 部分木のサイズ]. 子が存在しない場合はNone
        """
        return [None, None, 0]

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
                node[bit] = self._new_node()

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

    def get_min_element(self) -> Optional[int]:
        """最小値を返す

        Returns:
            Optional[int]: 最小値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) == 0:
            return None

        digit = self.bit_size
        min_element = 0

        node = self.root
        while digit >= 0:
            # 左の子が存在する場合は左の子を選択
            if (node[0] is not None) and (node[0][-1] != 0):
                node = node[0]
            else:
                node = node[1]
                min_element |= 1 << digit

            digit -= 1

        return min_element

    def get_max_element(self) -> Optional[int]:
        """最大値を返す

        Returns:
            Optional[int]: 最大値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) == 0:
            return None

        digit = self.bit_size
        max_element = 0

        node = self.root
        while digit >= 0:
            # 右の子が存在する場合は右の子を選択
            if (node[1] is not None) and (node[1][-1] != 0):
                node = node[1]
                max_element |= 1 << digit
            else:
                node = node[0]

            digit -= 1

        return max_element

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

    def get_max_element_xor(self, x: int) -> Optional[int]:
        """xとxorが最大となる値を返す

        Args:
            x (int): xorする値

        Returns:
            Optional[int]: xとxorが最大となる値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) == 0:
            return None

        digit = self.bit_size
        max_element = 0

        node = self.root
        while digit >= 0:
            # x[digit] = 1 の場合, 左の子が最大
            if (x >> digit) & 1:
                if (node[0] is not None) and (node[0][-1] != 0):
                    node = node[0]
                else:
                    node = node[1]
                    max_element |= 1 << digit
            else:
                if (node[1] is not None) and (node[1][-1] != 0):
                    node = node[1]
                    max_element |= 1 << digit
                else:
                    node = node[0]

            digit -= 1

        return max_element

    def get_kth_smallest_element(self, k: int) -> Optional[int]:
        """k番目に小さい値を返す

        Args:
            k (int): k番目 (1-indexed)

        Returns:
            Optional[int]: k番目に小さい値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) < k:
            return None

        digit = self.bit_size
        kth_element = 0

        node = self.root
        while digit >= 0:
            # 左の子の個数
            left_child = 0 if node[0] is None else node[0][-1]

            # 右の子を選択する場合
            if left_child < k:
                node = node[1]
                k -= left_child
                kth_element |= 1 << digit
            else:
                node = node[0]

            digit -= 1

        return kth_element

    def get_kth_largest_element(self, k: int) -> Optional[int]:
        """k番目に大きい値を返す

        Args:
            k (int): k番目 (1-indexed)

        Returns:
            Optional[int]: k番目に大きい値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) < k:
            return None

        return self.get_kth_smallest_element(len(self) - k + 1)

    def get_kth_smallest_element_xor(self, x: int, k: int) -> Optional[int]:
        """xとxorしたときに, k番目に小さい値を返す

        Args:
            x (int): xorする値
            k (int): k番目 (1-indexed)

        Returns:
            Optional[int]: xとxorしたときにk番目に小さい値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) < k:
            return None

        digit = self.bit_size
        kth_element = 0

        node = self.root
        while digit >= 0:
            # x[digit] = 1 の場合, 右の子が最小
            if (x >> digit) & 1:
                right_child = 0 if node[1] is None else node[1][-1]
                # 右の子がkに満たない -> 左
                if right_child < k:
                    node = node[0]
                    k -= right_child
                else:
                    node = node[1]
                    kth_element |= 1 << digit
            else:
                left_child = 0 if node[0] is None else node[0][-1]
                # 左の子がkに満たない -> 右
                if left_child < k:
                    node = node[1]
                    k -= left_child
                    kth_element |= 1 << digit
                else:
                    node = node[0]

            digit -= 1

        return kth_element

    def get_kth_largest_element_xor(self, x: int, k: int) -> Optional[int]:
        """xとxorしたときに, k番目に大きい値を返す

        Args:
            x (int): xorする値
            k (int): k番目 (1-indexed)

        Returns:
            Optional[int]: xとxorしたときにk番目に大きい値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        if len(self) < k:
            return None

        return self.get_kth_smallest_element_xor(x, len(self) - k + 1)

    def pop_min_element(self) -> Optional[int]:
        """最小値を削除して返す

        Returns:
            Optional[int]: 最小値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        min_element = self.get_min_element()

        if min_element is None:
            return None

        self.discard(min_element)
        return min_element

    def pop_max_element(self) -> Optional[int]:
        """最大値を削除して返す

        Returns:
            Optional[int]: 最大値. 存在しない場合はNone

        TimeComplexity:
            O(bit_size)
        """
        max_element = self.get_max_element()

        if max_element is None:
            return None

        self.discard(max_element)
        return max_element

    # TODO: 実装
    def next_value(self, lower: int) -> Optional[int]:
        ...

    # TODO: 実装
    def prev_value(self, upper: int) -> Optional[int]:
        ...

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
