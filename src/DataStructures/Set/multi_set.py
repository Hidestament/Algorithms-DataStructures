from typing import Optional
from heapq import heappush, heappop
from collections import defaultdict


class MultiSet:
    """Priority Queueを使用した多重集合

    Attributes:
        min_hq (list): 最小値を取得するためのヒープキュー
        max_hq (list): 最大値を取得するためのヒープキュー
        counter (dict): 要素の個数を管理する辞書

    Methods:
        insert(x): xを追加する
        discard(x, k=1): xをk個削除する
        get_min_element(): 最小値を取得する
        get_max_element(): 最大値を取得する
        pop_min(): 最小値を削除する
        pop_max(): 最大値を削除する
        __contains__(x): xが含まれているかどうかを返す
    """

    def __init__(self):
        self.min_hq = []
        self.max_hq = []
        self.counter = defaultdict(int)

    def insert(self, x: int):
        """xを追加する

        Args:
            x (int): 追加する値
        """
        heappush(self.min_hq, x)
        heappush(self.max_hq, -x)
        self.counter[x] += 1

    def discard(self, x: int, k: int = 1):
        """xをk個削除する

        Args:
            x (int): 削除する値
            k (int): 削除する個数

        Notes:
            xの個数がk個未満の場合, xをすべて削除する
            xが存在しない場合は何もしない
        """
        if self.counter[x] == 0:
            return

        self.counter[x] = max(0, self.counter[x] - k)
        # 0番目の要素が常に存在するように更新する
        while self.min_hq:
            if self.counter[self.min_hq[0]] == 0:
                heappop(self.min_hq)
            else:
                break

        while self.max_hq:
            if self.counter[-1 * self.max_hq[0]] == 0:
                heappop(self.max_hq)
            else:
                break

    def get_min_element(self) -> Optional[int]:
        """最小値を取得する

        Returns:
            Optional[int]: 最小値. 要素がない場合はNone
        """
        if self.min_hq:
            return self.min_hq[0]

    def get_max_element(self) -> Optional[int]:
        """最大値を取得する

        Returns:
            Optional[int]: 最大値. 要素がない場合はNone
        """
        if self.max_hq:
            return -1 * self.max_hq[0]

    def pop_min(self) -> Optional[int]:
        """最小値を削除する

        Returns:
            Optional[int]: 削除した最小値. 削除する値がない場合はNone
        """
        min_element = self.get_min_element()

        if min_element is not None:
            self.discard(min_element)

        return min_element

    def pop_max(self) -> Optional[int]:
        """最大値を削除する

        Returns:
            Optional[int]: 削除した最大値. 削除する値がない場合はNone
        """
        max_element = self.get_max_element()

        if max_element is not None:
            self.discard(max_element)

        return max_element

    def __contains__(self, x: int) -> bool:
        """xが含まれているかどうかを返す

        Args:
            x (int): 検索する値

        Returns:
            bool: xが含まれているかどうか

        TimeComplexity:
            O(1)
        """
        return True if self.cnt[x] > 0 else False
