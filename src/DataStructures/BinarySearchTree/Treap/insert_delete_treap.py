from typing import Optional, Generator
from collections import deque
from random import random


class TreapNode:
    """Treapのノード

    Attributes:
        key (int): 二分探索木のノードに格納される要素のkey
        left (Optional[TreapNode]): 二分探索木のノードの左の子
        right (Optional[TreapNode]): 二分探索木のノードの右の子
        count (int): このノードの個数 (多重集合の場合)
        subtree_size (int): このノードを根とする部分木の要素数
        priority (float): このノードの優先度

    Note:
        data(value)は載せてない
    """

    def __init__(self, key: int, count: int = 1):
        self.key = key
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None
        self.count = count
        self.subtree_size = count
        self.priority = random()

    def _update(self):
        """このノードを根とする部分木の要素数を更新する (親は更新しない)
        """
        left_size = self.left.subtree_size if self.left is not None else 0
        right_size = self.right.subtree_size if self.right is not None else 0
        self.subtree_size = left_size + right_size + self.count

    def __repr__(self) -> str:
        return f"TreapNode(key={self.key}, priority={self.priority}, count={self.count})"


class Treap:
    """基本的なTreap (非再帰, Insert/Delete Based). 計算時間の期待値は全てO(log N)

    Attributes:
        root (Optional[TreapNode]): 二分探索木の根

    Methods:
        __contains__(self, key: int): keyが二分探索木に含まれているかどうかを返す
        search(key: int): 存在するならば二分探索木に要素k(key kを持つ要素)を返す
        get(key: int): 存在するならば二分探索木に要素k(key kを持つ要素)を返す
        count(key: int): 二分探索木に含まれるkeyの個数を返す
        insert(key: int, num: int): 二分探索木に要素k(key kを持つ要素)を挿入する
        delete(key: int, num: int): 二分探索木から要素k(key kを持つ要素)を削除する
        min_element(): 二分探索木の最小要素を返す
        max_element(): 二分探索木の最大要素を返す
        lower_bound(key: int): key <= x.key となる最小のxを返す
        upper_bound(key: int): x.key <= key となる最大のxを返す
        kth_smallest_element(k: int): 二分探索木の中間順巡回でk番目に小さい要素を返す
        kth_largest_element(k: int): 二分探索木の中間順巡回でk番目に大きい要素を返す
        inorder(): 二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)
        preorder(): 二分探索木の先行順巡回 (二分探索木の要素を出力する)

    Notes:
        ヒープ条件: 親のpriority >= 子のpriority
    """

    def __init__(self):
        """初期化
        """
        self.root = None

    def __len__(self) -> int:
        """二分探索木の要素数を返す

        Returns:
            int: 二分探索木の要素数
        """
        return self.root.subtree_size if self.root is not None else 0

    def _new_node(self, key: int, count: int = 1) -> TreapNode:
        return TreapNode(key, count)

    def _update(self, path: list[TreapNode]):
        """node -> root上の各頂点の情報を更新

        Args:
            path (list[TreapNode]): [root ... -> ... node]
        """
        for node in reversed(path):
            node._update()

    def _rotate_and_update(self, path: list[TreapNode]):
        """node -> root上の各頂点の情報を更新 & ヒープ条件が満たされるように回転させる

        Args:
            path (list[TreapNode]): [root ... -> ... node]
        """
        assert len(path) >= 1

        _path = path[::-1] + [None]
        for node, parent in zip(_path, _path[1:]):
            node._update()

            left_priority = node.left.priority if node.left is not None else -float("inf")
            right_priority = node.right.priority if node.right is not None else -float("inf")

            # 右回転
            if node.priority < left_priority:
                self._rotate_right(node, parent)
            # 左回転
            elif node.priority < right_priority:
                self._rotate_left(node, parent)

    def _rotate_right(self, node: TreapNode, parent: Optional[TreapNode]) -> TreapNode:
        """nodeを根とする部分木を右回転させる

        Args:
            node (TreapNode): 回転させたい部分木の根
            parent (Optional[TreapNode]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            TreapNode: 回転後の部分木の根

        Notes:
            nodeの左の子が存在することを前提とする
        """
        assert node.left

        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        if parent is None:
            self.root = new_root
        elif parent.key < node.key:
            parent.right = new_root
        else:
            parent.left = new_root

        node._update()
        new_root._update()
        return new_root

    def _rotate_left(self, node: TreapNode, parent: Optional[TreapNode]) -> TreapNode:
        """nodeを根とする部分木を左回転させる

        Args:
            node (TreapNode): 回転させたい部分木の根
            parent (Optional[TreapNode]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            TreapNode: 回転後の部分木の根

        Notes:
            nodeの右の子が存在することを前提とする
        """
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        if parent is None:
            self.root = new_root
        elif parent.key < node.key:
            parent.right = new_root
        else:
            parent.left = new_root

        node._update()
        new_root._update()
        return new_root

    def _search_with_path(self, key: int) -> list[TreapNode]:
        """keyを持つ要素を二分探索木から探索する (探索パスを返す)

        Args:
            key (int): 探索したい要素のkey

        Returns:
            list[TreapNode]: 探索パス
        """
        if self.root is None:
            return []

        node = self.root
        path = []
        while node is not None:
            path.append(node)
            if node.key == key:
                break
            elif node.key < key:
                node = node.right
            else:
                node = node.left
        return path

    def search(self, key: int) -> Optional[TreapNode]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (int): 探索したい要素のkey

        Returns:
            Optional[TreapNode]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None
        node = self._search_with_path(key)[-1]
        return node if node.key == key else None

    def get(self, key: int) -> Optional[TreapNode]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (int): 探索したい要素のkey

        Returns:
            Optional[TreapNode]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        return self.search(key)

    def count(self, key: int) -> int:
        """二分探索木に含まれるkeyの個数を返す

        Args:
            key (int): 二分探索木に含まれるkey

        Returns:
            int: 二分探索木に含まれるkeyの個数
        """
        node = self.search(key)
        return node.count if node is not None else 0

    def insert(self, key: int, num: int = 1):
        """二分探索木に要素を挿入する

        Args:
            key (int): 挿入したい要素のkey. 重複を許す.
            num (int): 挿入したい要素の個数. Defaults to 1.
        """
        if self.root is None:
            self.root = self._new_node(key, num)
            return

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            parent = node
            node = self._new_node(key, num)
            path.append(node)
            if parent.key < key:
                parent.right = node
            else:
                parent.left = node
        else:
            node.count += num

        self._rotate_and_update(path)

    def delete(self, key: int, num: int = 1):
        """二分探索木から要素を削除する

        Args:
            key (int): 削除したい要素のkey, Noneはmerge, splitのためのダミー
            num (int): 削除したい要素の個数. Defaults to 1.
        """
        if self.root is None:
            return

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            return

        node.count = max(0, node.count - num)

        # 削除しても要素が残る場合
        if node.count > 0:
            self._update(path)
            return

        path.pop()
        parent = path[-1] if len(path) >= 1 else None
        # 子が1つ以下になるまで回転
        while (node.left is not None) or (node.right is not None):
            left_priority = node.left.priority if node.left is not None else -float("inf")
            right_priority = node.right.priority if node.right is not None else -float("inf")

            # 子のうち, priorityが高い方に回転する
            if left_priority > right_priority:
                parent = self._rotate_right(node, parent)
            else:
                parent = self._rotate_left(node, parent)

            if parent is not None:
                path.append(parent)

        # 削除
        if parent is None:
            self.root = None
        elif parent.left is node:
            parent.left = None
        else:
            parent.right = None

        del node

        self._update(path)
        return

    def _min_element_with_parent(self, root: TreapNode) -> list[TreapNode]:
        """rootを根とする部分木の最小要素を返す (pathも返す)

        Args:
            root (TreapNode): 根

        Returns:
            list[TreapNode]: 最小要素に至る探索パス
        """
        node = root
        path = []
        while node is not None:
            path.append(node)
            node = node.left
        return path

    def min_element(self) -> Optional[TreapNode]:
        """二分探索木の最小要素を返す

        Returns:
            Optional[TreapNode]: 二分探索木の最小要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._min_element_with_parent(self.root)[-1]

    def _max_element_with_parent(self, root: TreapNode) -> list[TreapNode]:
        """rootを根とする部分木の最大要素を返す (pathも返す)

        Args:
            root (TreapNode): 根

        Returns:
            list[TreapNode]: 最大要素に至る探索パス
        """
        node = root
        path = []
        while node is not None:
            path.append(node)
            node = node.right
        return path

    def max_element(self) -> Optional[TreapNode]:
        """二分探索木の最大要素を返す

        Returns:
            Optional[TreapNode]: 二分探索木の最大要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._max_element_with_parent(self.root)[-1]

    def lower_bound(self, key: int) -> Optional[TreapNode]:
        """key <= x.key となる最小のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[TreapNode]: key <= x.key となる最小のx. 存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        # 最小値なので, 基本的に左に進む
        node = self.root
        # 条件を満たす最小node
        minimum = None
        while node is not None:
            if node.key == key:
                return node
            elif node.key < key:
                node = node.right
            else:
                if (minimum is None) or (node.key < minimum.key):
                    minimum = node

                node = node.left

        return minimum

    def upper_bound(self, key: int) -> Optional[TreapNode]:
        """x.key <= keyとなる最大のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[TreapNode]: x.key <= keyとなる最大のx. 存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        # 最大値なので, 基本的に右に進む
        node = self.root
        # 条件を満たす最大のnode
        maximum = None
        while node is not None:
            if node.key == key:
                return node
            elif node.key > key:
                node = node.left
            else:
                if (maximum is None) or (maximum.key < node.key):
                    maximum = node
                node = node.right

        return maximum

    def kth_smallest_element(self, k: int) -> Optional[TreapNode]:
        """二分探索木の中間順巡回でk番目に小さい要素を返す

        Args:
            k (int): k番目に小さい要素 (kは1-indexed)

        Returns:
            Optional[TreapNode]: 二分探索木の中間順巡回でk番目に小さい要素. 存在しない場合はNoneを返す
        """
        if len(self) < k:
            return None

        node = self.root
        while node is not None:
            left = node.left.subtree_size if node.left is not None else 0
            # そのnodeに含まれる場合
            if left < k <= left + node.count:
                return node
            # 左に含まれる場合
            if k <= left:
                node = node.left
            # 右に含まれる場合
            else:
                k -= (left + node.count)
                node = node.right

        return None

    def kth_largest_element(self, k: int) -> Optional[TreapNode]:
        """二分探索木の中間順巡回でk番目に大きい要素を返す

        Args:
            k (int): k番目に大きい要素 (kは1-indexed)

        Returns:
            Optional[TreapNode]: 二分探索木の中間順巡回でk番目に大きい要素. 存在しない場合はNoneを返す
        """
        if len(self) < k:
            return None
        return self.kth_smallest_element(len(self) - k + 1)

    def __contains__(self, key: int) -> bool:
        """keyが二分探索木に含まれているかどうかを返す

        Args:
            key (int): 二分探索木に含まれているかどうかを調べたい要素のkey

        Returns:
            bool: keyが二分探索木に含まれているかどうか
        """
        return True if self.search(key) is not None else False

    def inorder(self) -> Generator[TreapNode, None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[TreapNode, None, None]: 二分探索木の中間順巡回で得られる要素
        """
        if self.root is None:
            return

        dq = deque([[self.root, False]])
        while dq:
            node, flag = dq[-1]

            # nodeを既に1回探索済なら, nodeを出力しての右の子へ
            if flag:
                node, _ = dq.pop()
                yield node

                if node.right is not None:
                    dq.append([node.right, False])
                continue

            dq[-1][1] = True

            # nodeを未探索なら, 左の子へ
            if node.left is not None:
                dq.append([node.left, False])

    def preorder(self) -> Generator[TreapNode, None, None]:
        """二分探索木の先行順巡回 (二分探索木の要素を出力する)

        Yields:
            Generator[TreapNode, None, None]: 二分探索木の先行順巡回で得られる要素
        """
        if self.root is None:
            return

        dq = deque([self.root])
        while dq:
            node = dq.pop()

            if node is None:
                continue

            yield node

            # 先に右の子を追加しておく
            dq.append(node.right)
            dq.append(node.left)
