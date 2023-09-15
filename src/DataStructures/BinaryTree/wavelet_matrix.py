from typing import Optional
from heapq import heappush, heappop

from src.DataStructures.BitVector.bit_vector_accumulate import BitVectorAcc as BitVector


class WaveletMatrix:
    """数列に関するクエリを高速に処理する

    Notation:
        T: 元の配列.
        T[i]: 元の配列のi番目の要素.
        x: Tの要素.
        B[j]: j番目のBit Vector.
        bit_size: log2(Tの最大値)

    Attributes:
        bit_size (int): WaveletMatrixの列数 (深さ).
        wavelet_matrix (list[BitVector]): WaveletMatrix.

    Methods:
        access(i): T[i], O(bit_size).
        rank(x, right): T[0..right)におけるxの出現回数, O(bit_size).
        rank_range(x, left, right): T[left..right)におけるxの出現回数, O(bit_size).
        select(x, k): Tのk個目のxの出現位置, O(bit_size).
        quantile(left, right, k): T[left..right)の中のk番目に小さい値, O(bit_size).
        kth_smallest(left, right, k): T[left..right)の中でk番目に小さい要素, O(bit_size).
        kth_largest(left, right, k): T[left..right)の中でk番目に大きい要素, O(bit_size).
        topk(left, right, k): T[left..right)の中で出現回数が多い順に(要素, 出現回数)をk個.
        sum(left, right): T[left..right)の和.
        range_freq(left, right, lower, upper): T[left..right)の中で, lower <= x < upper となるxの個数, O(bit_size).
        prev_value(left, right, upper): T[left..right)の中で x < upperを満たす最大のx, O(bit_size).
        next_value(left, right, lower): T[left..right)の中で lower <= x を満たす最小のx, O(bit_size).
    """

    def __init__(self, T: list[int]):
        """WaveletMatrix

        Args:
            T (list[int]): 整数列

        TimeComplexity:
            構築にO(len(T) * bit_size)
        """
        self.bit_size: int = max(T).bit_length() if T else 0
        self.wavelet_matrix: list[BitVector] = self._build(T)

    def _build(self, T: list[int]) -> list[BitVector]:
        """WaveletMatrixを構築する

        Args:
            T (list[int]): 元の配列

        Returns:
            list[BitVector]: WaveletMatrix

        TimeComplexity:
            O(len(T) * bit_size)
        """
        wavelet_matrix: list[BitVector] = []
        for digit in range(self.bit_size)[::-1]:
            zeros = [t for t in T if not self._get_i_bit(t, digit + 1)]
            ones = [t for t in T if self._get_i_bit(t, digit + 1)]

            T = zeros + ones
            wavelet_matrix.append(BitVector([self._get_i_bit(t, digit) for t in T]))
        return wavelet_matrix

    def __len__(self) -> int:
        """len(T).

        Returns:
            int: len(T)

        TimeComplexity:
            O(1)
        """
        if len(self.wavelet_matrix) == 0:
            return 0
        return len(self.wavelet_matrix[0])

    def __getitem__(self, i: int) -> int:
        """元の配列T[i]を返す

        Args:
            i (int): index

        Returns:
            int: T[i]

        TimeComplexity:
            O(bit_size)
        """
        return self.access(i)

    def _get_i_bit(self, x: int, digit: int) -> int:
        """xの(下から数えて)digit桁目のbitを計算

        Args:
            x (int): 整数
            digit (int): 桁数

        Returns:
            int: 0 or 1
        """
        return 1 & (x >> digit)

    def _next_range(self, B: BitVector, bit: int, left: int, right: int) -> (int, int):
        """B[j][left..right)におけるbit(0 or 1)が, B[j+1]においてどの範囲になるかを計算

        Args:
            B (BitVector): Bit Vector B[j].
            bit (int): 範囲に含まれるbit. 0 or 1.
            left (int): Bの範囲の下限.
            right (int): Bの範囲の上限.

        Returns:
            (int, int): B[j+1]の[left..right)

        TimeComplexity:
            O(1)
        """
        if bit == 0:
            left = B.rank0(left)
            right = B.rank0(right)
        else:
            left = B.rank0_all() + B.rank1(left)
            right = B.rank0_all() + B.rank1(right)
        return (left, right)

    def access(self, i: int) -> int:
        """元の配列T[i]を返す

        Args:
            i (int): index

        Returns:
            int: T[i]

        TimeComplexity:
            O(bit_size)
        """
        x = 0
        for digit, B in enumerate(self.wavelet_matrix):
            bit = B[i]
            x |= bit << (self.bit_size - digit - 1)

            if bit == 0:
                i = B.rank0(i + 1) - 1
            else:
                i = B.rank0_all() + B.rank1(i + 1) - 1
        return x

    def rank(self, x: int, right: int) -> int:
        """T[0..right)における, xの出現回数を返す

        Args:
            x (int): 対象の要素
            right (int): Tの範囲の上限

        Returns:
            int: 出現回数

        TimeComplexity:
            O(bit_size)
        """
        return self.rank_range(x, 0, right)

    def rank_range(self, x: int, left: int, right: int) -> int:
        """T[left..right)におけるxの出現回数を返す

        Args:
            x (int): 対象の要素
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限

        Returns:
            int: 出現回数

        TimeComplexity:
            O(bit_size)
        """
        if (left >= right) or (x.bit_length() > self.bit_size) or (x < 0):
            return 0

        left = max(left, 0)
        right = min(right, len(self))
        for digit, B in enumerate(self.wavelet_matrix):
            x_bit = self._get_i_bit(x, self.bit_size - digit - 1)
            left, right = self._next_range(B, x_bit, left, right)
        return right - left

    def select(self, x: int, k: int) -> Optional[int]:
        """元の配列Tのk個目のxの出現位置 (index) を返す

        Args:
            x (int): 対象の要素.
            k (int): 何個目の出現か. 1-index.

        Returns:
            Optional[int]: index. 該当要素が存在しない場合はNone.

        TimeComplexity:
            O(bit_size)
        """
        if not (0 <= x < 1 << self.bit_size):
            return None
        if k <= 0:
            return None

        # xが最終的な配列のどの範囲に入るか計算
        left, right = 0, len(self)
        for digit, B in enumerate(self.wavelet_matrix):
            x_bit = self._get_i_bit(x, self.bit_size - digit - 1)
            left, right = self._next_range(B, x_bit, left, right)

        if left >= right:
            return None

        # 上記範囲のk番目が, 元の配列で何番目か計算
        index = left + k - 1
        for digit, B in enumerate(self.wavelet_matrix[::-1]):
            if index is None:
                return None

            x_bit = self._get_i_bit(x, digit)
            if x_bit == 0:
                index = B.select0(index + 1)
            else:
                index = B.select1(index - (B.rank0_all() - 1))
        return index

    def quantile(self, left: int, right: int, k: int) -> Optional[int]:
        """元の配列T[left..right)の中のk番目に小さい値を返す

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            k (int): 何番目の要素か, 1-index

        Returns:
            Optional[int]: k番目に小さい値. 該当要素が存在しない場合はNone.

        TimeComplexity:
            O(bit_size)
        """
        if (left >= right) or (k <= 0) or (right - left < k):
            return None

        left = max(left, 0)
        right = min(right, len(self))

        x = 0
        for digit, B in enumerate(self.wavelet_matrix):
            num_zeros = B.rank0(right) - B.rank0(left)

            # 該当要素が0の中か or 1の中か
            bit = 0 if k <= num_zeros else 1
            left, right = self._next_range(B, bit, left, right)

            if bit == 1:
                k -= num_zeros
                x |= bit << (self.bit_size - digit - 1)
        return x

    def kth_smallest(self, left: int, right: int, k: int) -> Optional[int]:
        """T[left..right)の中で, k番目に小さい要素を返す.

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            k (int): 何番目の要素か, 1-index

        Returns:
            Optional[int]: k番目に小さい値. 該当要素が存在しない場合はNone.

        TimeComplexity:
            O(bit_size)
        """
        return self.quantile(left, right, k)

    def kth_largest(self, left: int, right: int, k: int) -> Optional[int]:
        """T[left..right)の中で, k番目に大きい要素を返す.

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            k (int): 何番目の要素か, 1-index

        Returns:
            Optional[int]: k番目に大きい要素. 存在しない場合None.

        TimeComplexity:
            O(bit_size)
        """
        return self.quantile(left, right, right - left - k + 1)

    def topk(self, left: int, right: int, k: int) -> list[tuple[int, int]]:
        """T[left..right)の中で, 出現回数が多い順に(要素, 出現回数)をk個返す.

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            k (int): いくつ返すか, 1-index

        Returns:
            list[tuple[int, int]]: [(出現回数が1番多い要素, その出現回数), ...]

        Note:
            - 出現回数が同じものは, 値が小さいものが先に返る
            - k個未満の場合, 全て返す

        TimeComplexity:
            TODO: ?????
        """
        if (left >= right) or (k <= 0):
            return []

        left = max(left, 0)
        right = min(right, len(self))

        # (長さ, 要素の値, left, right, B[j])
        hq: list[tuple[int, int, int, int, int]] = []
        heappush(hq, (-(right - left), 0, left, right, 0))

        topk = []
        while hq:
            if len(topk) == k:
                break

            _, x, left, right, j = heappop(hq)

            if j == self.bit_size:
                if right - left > 0:
                    topk.append((x, right - left))
                continue

            B = self.wavelet_matrix[j]

            zero_left, zero_right = self._next_range(B, 0, left, right)
            heappush(hq, (-(zero_right - zero_left), x, zero_left, zero_right, j + 1))

            one_left, one_right = self._next_range(B, 1, left, right)
            x |= 1 << (self.bit_size - j - 1)
            heappush(hq, (-(one_right - one_left), x, one_left, one_right, j + 1))

        return topk

    def sum(self, left: int, right: int) -> int:
        """T[left..right)の和

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限

        Returns:
            int: ΣT[left..right)

        TimeComplexity:
            TODO: ????
        """
        if left >= right:
            return 0

        topk = self.topk(left, right, right - left + 1)
        s = sum(x * cnt for x, cnt in topk)
        return s

    def range_freq_to(self, left: int, right: int, upper: int) -> int:
        """T[left..right)の0 <= x < upper となるxの個数を計算する

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            upper (int): 要素の上限

        Returns:
            int: 0 <= x < upperとなる要素の数

        TimeComplexity:
            O(bit_size)
        """
        if (left >= right) or (upper <= 0):
            return 0

        # 全ての要素が < upper
        if upper.bit_length() > self.bit_size:
            return right - left

        cnt = 0
        left = max(left, 0)
        right = min(right, len(self))
        for digit, B in enumerate(self.wavelet_matrix):
            upper_bit = self._get_i_bit(upper, self.bit_size - digit - 1)
            if upper_bit == 1:
                cnt += B.rank0(right) - B.rank0(left)

            left, right = self._next_range(B, upper_bit, left, right)

        return cnt

    def range_freq_from(self, left: int, right: int, lower: int) -> int:
        """T[left..right)のlower <= x となるxの個数を計算する

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            lower (int): 要素の下限

        Returns:
            int: lower <= x となる要素の数

        TimeComplexity:
            O(bit_size)
        """
        if (left >= right) or (lower > (1 << self.bit_size)):
            return 0

        left = max(left, 0)
        right = min(right, len(self))
        return (right - left) - self.range_freq_to(left, right, lower)

    def range_freq(self, left: int, right: int, lower: int, upper: int) -> int:
        """T[left..right)のlower <= x < upper となるxの個数を計算する

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            lower (int): 要素の下限
            upper (int): 要素の上限

        Returns:
            int: lower <= x < upperとなる要素の数

        TimeComplexity:
            O(bit_size)
        """
        if (left >= right) or (lower >= upper) or (lower > (1 << self.bit_size)):
            return 0

        return self.range_freq_to(left, right, upper) - self.range_freq_to(
            left, right, lower
        )

    # TODO: 実装
    def range_list(self, left: int, right: int, lower: int, upper: int):
        """T[left..right)の中で, lower <= x < upperを満たすxを頻度とともに返す

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            lower (int): 要素の下限
            upper (int): 要素の上限

        Returns:
            TODO: ????

        TimeComplexity:
            TODO: ???
        """
        ...

    def prev_value(self, left: int, right: int, upper: int) -> Optional[int]:
        """T[left..right)の中で, 0 <= x < upperを満たす最大のxを返す

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            upper (int): 要素の上限

        Returns:
            Optional[int]: 0 <= x < upperを満たす最大のx. 存在しない場合None.

        TimeComplexity:
            O(bit_size)
        """
        # T[left..right)内の, 0 <= x < upperのxの個数
        cnt = self.range_freq_to(left, right, upper)
        if cnt == 0:
            return None
        return self.quantile(left, right, cnt)

    def next_value(self, left: int, right: int, lower: int) -> int:
        """T[left..right)の中で, lower <= x を満たす最小のxを返す

        Args:
            left (int): Tの範囲の下限
            right (int): Tの範囲の上限
            lower (int): 要素の下限

        Returns:
            int: lower <= x を満たす最小のx

        TimeComplexity:
            O(bit_size)
        """
        # T[left..right)内の, lower <= xとなるxの個数
        cnt = self.range_freq_from(left, right, lower)
        if cnt == 0:
            return None
        return self.quantile(left, right, right - left - cnt + 1)
