# https://judge.yosupo.jp/submission/161374
# 平均的には辞書より遅いが, 変なケースでは辞書より速い (https://judge.yosupo.jp/submission/161376)
# src/DataStructures/BinarySearchTree/test_treap_hashmap.pyを修正したもの

import sys
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
        priority (float): このノードの優先度
    """

    def __init__(self, key: K, value: V):
        self.value = value
        self.key = key
        self.left: Optional[TreapNode[K, V]] = None
        self.right: Optional[TreapNode[K, V]] = None
        self.priority = random()

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
        __contains__(key: K): keyが二分探索木に含まれているかどうかを返す
        get(key: K, default: Optional[V]): key=kを持つvalueを返す. 存在しないならdefaultを返す
        pop(key: K, default: Optional[V]): key=kを持つ要素を削除してそのvalue返す. 存在しないならdefaultを返す.
        keys(): 二分探索木のkeyを昇順に出力する.
        values(): 二分探索木のvalueをkeyに関する昇順に出力する.
        items(): 二分探索木の(key, value)をkeyに関する昇順に出力する.
        insert(key: K): 二分探索木に要素k(key kを持つ要素)を挿入する
        delete(key: K): 二分探索木から要素k(key kを持つ要素)を削除する

    Notes:
        ヒープ条件: 親のpriority >= 子のpriority
    """

    def __init__(self):
        """初期化
        """
        self.root = None

    def _new_node(
        self,
        key: K,
        value: V,
    ) -> TreapNode[K, V]:
        return TreapNode(key, value)

    def _rotate(self, path: list[TreapNode[K, V]]):
        """node -> root上の各頂点の情報を更新 & ヒープ条件が満たされるように回転させる

        Args:
            path (list[TreapNode[K, V]]): [root ... -> ... node]
        """
        assert len(path) >= 1

        _path = path[::-1] + [None]
        for node, parent in zip(_path, _path[1:]):
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

        self._rotate(path)

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
        return return_value

    def delete(self, key: K):
        """二分探索木から要素を削除する

        Args:
            key (K): 削除したい要素のkey
        """
        self.pop(key)

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


input = sys.stdin.readline


Q = int(input())
tree = TreapHashMap[int, int]()

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        k, v = query[1:]
        tree[k] = v
    else:
        k = query[1]
        print(tree.get(k, 0))
