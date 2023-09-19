from typing import Optional, Generator, TypeVar, Generic
from collections import deque
from random import random


K = TypeVar("K")
V = TypeVar("V")


class TreapNode(Generic[K, V]):
    """Treapのノード

    Args:
        K: 二分探索木のノードに格納される要素のkeyの型 (比較可能である必要がある)
        V: 二分探索木のノードに格納される要素のvalueの型

    Attributes:
        key (K): 二分探索木のノードに格納される要素のkey
        value (T): 二分探索木のノードに格納される要素
        left (Optional[TreapNode[K, V]]): 二分探索木のノードの左の子
        right (Optional[TreapNode[K, V]]): 二分探索木のノードの右の子
        subtree_size (int): このノードを根とする部分木の要素数
        priority (float): このノードの優先度
    """

    def __init__(self, key: K, value: V):
        self.value = value
        self.key = key
        self.left: Optional[TreapNode[K, V]] = None
        self.right: Optional[TreapNode[K, V]] = None
        self.subtree_size = 1
        self.priority = random()

    def _update(self):
        """このノードを根とする部分木の要素数を更新する (親は更新しない)
        """
        left_size = self.left.subtree_size if self.left is not None else 0
        right_size = self.right.subtree_size if self.right is not None else 0
        self.subtree_size = left_size + right_size + 1

    def __repr__(self) -> str:
        return f"TreapNode(key={self.key}, value={self.value})"


class TreapHashMap(Generic[K, V]):
    """Treapを使用したハッシュマップ

    Args:
        K: 二分探索木のノードに格納される要素のkeyの型 (比較可能である必要がある)
        V: 二分探索木のノードに格納される要素のvalueの型

    Attributes:
        root (Optional[TreapNode[K, V]]): 二分探索木の根

    Methods:
        __getitem__(key: K): key=kを持つ要素のvalueを返す. 存在しないならKeyErrorをレイズ.
        __setitem__(key: K, value: V): key=kを持つ要素を挿入する. 既に存在する場合はvalueを上書きする.
        __len__(): 二分探索木の要素数を返す
        __contains__(key: K): keyが二分探索木に含まれているかどうかを返す
        get(key: K, default: Optional[V]): key=kを持つvalueを返す. 存在しないならdefaultを返す
        pop(key: K, default: Optional[V]): key=kを持つ要素を削除してそのvalue返す. 存在しないならdefaultを返す.
        keys(): 二分探索木のkeyを昇順に出力する.
        values(): 二分探索木のvalueをkeyに関する昇順に出力する.
        items(): 二分探索木の(key, value)をkeyに関する昇順に出力する.
        insert(key: K): 二分探索木に要素k(key kを持つ要素)を挿入する
        delete(key: K): 二分探索木から要素k(key kを持つ要素)を削除する
        min_element(): 二分探索木の最小要素を返す
        max_element(): 二分探索木の最大要素を返す
        lower_bound(key: K): key <= x.key となる最小のxを返す
        upper_bound(key: K): x.key <= key となる最大のxを返す
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

    def _new_node(
        self,
        key: K,
        value: V,
    ) -> TreapNode[K, V]:
        return TreapNode(key, value)

    def _update(self, path: list[TreapNode[K, V]]):
        """node -> root上の各頂点の情報を更新

        Args:
            path (list[TreapNode[K, V]]): [root ... -> ... node]
        """
        for node in reversed(path):
            node._update()

    def _rotate_and_update(self, path: list[TreapNode[K, V]]):
        """node -> root上の各頂点の情報を更新 & ヒープ条件が満たされるように回転させる

        Args:
            path (list[TreapNode[K, V]]): [root ... -> ... node]
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

    def _rotate_right(self, node: TreapNode[K, V], parent: Optional[TreapNode[K, V]]) -> TreapNode[K, V]:
        """nodeを根とする部分木を右回転させる

        Args:
            node (TreapNode[K, V]): 回転させたい部分木の根
            parent (Optional[TreapNode[K, V]]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            TreapNode[K, V]: 回転後の部分木の根

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

    def _rotate_left(self, node: TreapNode[K, V], parent: Optional[TreapNode[K, V]]) -> TreapNode[K, V]:
        """nodeを根とする部分木を左回転させる

        Args:
            node (TreapNode[K, V]): 回転させたい部分木の根
            parent (Optional[TreapNode[K, V]]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            TreapNode[K, V]: 回転後の部分木の根

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

    def _search_with_path(self, key: K) -> list[TreapNode[K, V]]:
        """keyを持つ要素を二分探索木から探索する (探索パスを返す)

        Args:
            key (K): 探索したい要素のkey

        Returns:
            list[TreapNode[K, V]]: 探索パス
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

    def search(self, key: K) -> Optional[TreapNode[K, V]]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (K): 探索したい要素のkey

        Returns:
            Optional[TreapNode[K, V]]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None
        node = self._search_with_path(key)[-1]
        return node if node.key == key else None

    def __getitem__(self, key: K) -> V:
        """keyを持つ要素を取得する

        Args:
            key (K): 取得したい要素のkey

        Returns:
            V: keyを持つ要素が存在すればその要素のvalueを返す. 存在しなければNoneを返す

        Raises:
            KeyError: keyを持つ要素が存在しない場合
        """
        node = self.search(key)
        if node is None:
            raise KeyError(f"Key: {key} is not found")
        return node.value

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """keyを持つ要素を取得する

        Args:
            key (K): 取得したい要素のkey
            default (Optional[V]): keyを持つ要素が存在しない場合のデフォルト値. Defaults to None.

        Returns:
            Optional[V]: keyを持つ要素が存在すればその要素のvalueを返す. 存在しなければdefaultを返す
        """
        node = self.search(key)
        return node.value if node is not None else default

    def __setitem__(self, key: K, value: V):
        self.insert(key, value)

    def insert(self, key: K, value: V):
        """二分探索木に要素を挿入する (既に存在する場合, valueを上書きする)

        Args:
            key (K): 挿入したい要素のkey.
            value (V): 挿入したい要素のvalue
        """
        if self.root is None:
            self.root = self._new_node(key, value)
            return

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            parent = node
            node = self._new_node(key, value)
            path.append(node)
            if parent.key < key:
                parent.right = node
            else:
                parent.left = node
        else:
            node.value = value

        self._rotate_and_update(path)

    def pop(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """二分探索木から要素を削除する

        Args:
            key (K): 削除したい要素のkey
            default (Optional[V]): keyが存在しない場合に返す値. Defaults to None.

        Returns:
            Optional[V]: 削除した要素のvalue. keyが存在しない場合はdefaultを返す
        """
        if self.root is None:
            return default

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            return default

        return_value = node.value
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
        return return_value

    def delete(self, key: K):
        """二分探索木から要素を削除する

        Args:
            key (K): 削除したい要素のkey
        """
        self.pop(key)

    def _min_element_with_parent(self, root: TreapNode[K, V]) -> list[TreapNode[K, V]]:
        """rootを根とする部分木の最小要素を返す (pathも返す)

        Args:
            root (TreapNode[K, V]): 根

        Returns:
            list[TreapNode[K, V]]: 最小要素に至る探索パス
        """
        node = root
        path = []
        while node is not None:
            path.append(node)
            node = node.left
        return path

    def min_element(self) -> Optional[TreapNode[K, V]]:
        """二分探索木の最小要素を返す

        Returns:
            Optional[TreapNode[K, V]]: 二分探索木の最小要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._min_element_with_parent(self.root)[-1]

    def _max_element_with_parent(self, root: TreapNode[K, V]) -> list[TreapNode[K, V]]:
        """rootを根とする部分木の最大要素を返す (pathも返す)

        Args:
            root (TreapNode[K, V]): 根

        Returns:
            list[TreapNode[K, V]]: 最大要素に至る探索パス
        """
        node = root
        path = []
        while node is not None:
            path.append(node)
            node = node.right
        return path

    def max_element(self) -> Optional[TreapNode[K, V]]:
        """二分探索木の最大要素を返す

        Returns:
            Optional[TreapNode[K, V]]: 二分探索木の最大要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._max_element_with_parent(self.root)[-1]

    def lower_bound(self, key: K) -> Optional[TreapNode[K, V]]:
        """key <= x.key となる最小のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[TreapNode[K, V]]: key <= x.key となる最小のx. 存在しない場合はNoneを返す
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

    def upper_bound(self, key: K) -> Optional[TreapNode[K, V]]:
        """x.key <= keyとなる最大のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[TreapNode[K, V]]: x.key <= keyとなる最大のx. 存在しない場合はNoneを返す
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

    def kth_smallest_element(self, k: int) -> Optional[TreapNode[K, V]]:
        """二分探索木の中間順巡回でk番目に小さい要素を返す

        Args:
            k (int): k番目に小さい要素 (kは1-indexed)

        Returns:
            Optional[TreapNode[K, V]]: 二分探索木の中間順巡回でk番目に小さい要素. 存在しない場合はNoneを返す
        """
        if len(self) < k:
            return None

        node = self.root
        while node is not None:
            left = node.left.subtree_size if node.left is not None else 0
            # そのnodeに含まれる場合
            if left < k <= left + 1:
                return node
            # 左に含まれる場合
            if k <= left:
                node = node.left
            # 右に含まれる場合
            else:
                k -= (left + 1)
                node = node.right

        return None

    def kth_largest_element(self, k: int) -> Optional[TreapNode[K, V]]:
        """二分探索木の中間順巡回でk番目に大きい要素を返す

        Args:
            k (int): k番目に大きい要素 (kは1-indexed)

        Returns:
            Optional[TreapNode[K, V]]: 二分探索木の中間順巡回でk番目に大きい要素. 存在しない場合はNoneを返す
        """
        if len(self) < k:
            return None
        return self.kth_smallest_element(len(self) - k + 1)

    def __contains__(self, key: K) -> bool:
        """keyが二分探索木に含まれているかどうかを返す

        Args:
            key (K): 二分探索木に含まれているかどうかを調べたい要素のkey

        Returns:
            bool: keyが二分探索木に含まれているかどうか
        """
        return True if self.search(key) is not None else False

    def keys(self) -> Generator[K, None, None]:
        """二分探索木のkeyを昇順に出力する.

        Yields:
            Generator[K, None, None]: 二分探索木のkeyを昇順に出力する
        """
        if self.root is None:
            return

        dq = deque([[self.root, False]])
        while dq:
            node, flag = dq[-1]

            # nodeを既に1回探索済なら, nodeを出力しての右の子へ
            if flag:
                node, _ = dq.pop()
                yield node.key

                if node.right is not None:
                    dq.append([node.right, False])
                continue

            dq[-1][1] = True

            # nodeを未探索なら, 左の子へ
            if node.left is not None:
                dq.append([node.left, False])

    def values(self) -> Generator[V, None, None]:
        """二分探索木のvalueをkeyに関する昇順に出力する.

        Yields:
            Generator[V, None, None]: 二分探索木のvalueをkeyに関する昇順に出力する
        """
        if self.root is None:
            return

        dq = deque([[self.root, False]])
        while dq:
            node, flag = dq[-1]

            # nodeを既に1回探索済なら, nodeを出力しての右の子へ
            if flag:
                node, _ = dq.pop()
                yield node.value

                if node.right is not None:
                    dq.append([node.right, False])
                continue

            dq[-1][1] = True

            # nodeを未探索なら, 左の子へ
            if node.left is not None:
                dq.append([node.left, False])

    def items(self) -> Generator[tuple[K, V], None, None]:
        """二分探索木の(key, value)をkeyに関する昇順に出力する.

        Yields:
            Generator[tuple[K, V], None, None]: 二分探索木の(key, value)をkeyに関する昇順に出力する
        """
        if self.root is None:
            return

        dq = deque([[self.root, False]])
        while dq:
            node, flag = dq[-1]

            # nodeを既に1回探索済なら, nodeを出力しての右の子へ
            if flag:
                node, _ = dq.pop()
                yield (node.key, node.value)

                if node.right is not None:
                    dq.append([node.right, False])
                continue

            dq[-1][1] = True

            # nodeを未探索なら, 左の子へ
            if node.left is not None:
                dq.append([node.left, False])

    def inorder(self) -> Generator[TreapNode[K, V], None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[TreapNode[K, V], None, None]: 二分探索木の中間順巡回で得られる要素
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

    def preorder(self) -> Generator[TreapNode[K, V], None, None]:
        """二分探索木の先行順巡回 (二分探索木の要素を出力する)

        Yields:
            Generator[TreapNode[K, V], None, None]: 二分探索木の先行順巡回で得られる要素
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
