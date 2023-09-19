from typing import Optional, Generator, TypeVar, Generic
from collections import deque


K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    """SplayTreeのノード

    Args:
        K: 二分探索木のノードに格納される要素のkeyの型 (比較可能である必要がある)
        V: 二分探索木のノードに格納される要素のvalueの型

    Attributes:
        key (K): 二分探索木のノードに格納される要素のkey
        value (T): 二分探索木のノードに格納される要素
        left (Optional[Node]): 左の子
        right (Optional[Node]): 右の子
    """

    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(key={self.key}, value={self.value})"


class DummyNode:
    """SplayTreeのダミーノード

    Attributes:
        left (Optional[Node]): 左の子
        right (Optional[Node]): 右の子
    """

    def __init__(self):
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class SplayHashMap(Generic[K, V]):
    """TowDown Splay Tree (非再帰)を用いたHashMap (SubtreeSizeを保持しない)

    Args:
        K: 二分探索木のノードに格納される要素のkeyの型 (比較可能である必要がある)
        V: 二分探索木のノードに格納される要素のvalueの型

    Attributes:
        root (Optional[Node[K, V]]): 二分探索木の根

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
        inorder(): 二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)
        preorder(): 二分探索木の先行順巡回 (二分探索木の要素を出力する)
    """

    def __init__(self):
        """初期化
        """
        self.root = None

    def _new_node(self, key: K, value: V) -> Node[K, V]:
        return Node(key, value)

    def _new_dummy_node(self) -> DummyNode:
        return DummyNode()

    def _splay(self, key: K, root: Optional[Node[K, V]], parent: Optional[Node[K, V]]) -> Optional[Node[K, V]]:
        """keyを持つ要素を二分探索木から探索する (TopDownSplay)

        Args:
            key (K): 探索したい要素のkey
            root (Optional[Node[K, V]]): 探索する部分木の根
            parent (Optional[Node[K, V]]): rootの親. Noneの場合はrootが根であることを意味する

        Returns:
            Optional[Node[K, V]]: 探索した要素. 存在しない場合はNoneを返す
        """
        if root is None:
            return

        dummy_root = self._new_dummy_node()
        left_node, right_node = dummy_root, dummy_root

        node = root
        while node is not None:
            if node.key == key:
                break
            elif key < node.key:
                if node.left is None:
                    break
                if key < node.left.key:
                    node = self._rotate_right(node)
                    if node.left is None:
                        break
                right_node.left = node
                right_node = node
                node = node.left
            else:
                if node.right is None:
                    break
                if key > node.right.key:
                    node = self._rotate_left(node)
                    if node.right is None:
                        break
                left_node.right = node
                left_node = node
                node = node.right

        right_node.left = node.right
        left_node.right = node.left

        node.left = dummy_root.right
        node.right = dummy_root.left

        if parent is None:
            self.root = node
        elif parent.key < node.key:
            self.root.right = node
        else:
            self.root.left = node

        return node

    def _rotate_right(self, node: Node[K, V]) -> Node[K, V]:
        """nodeを根とする部分木を右回転させる

        Args:
            node (Node[K, V]): 回転させたい部分木の根
            parent (Optional[Node[K, V]]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            Node[K, V]: 回転後の部分木の根

        Notes:
            nodeの左の子が存在することを前提とする
        """
        assert node.left

        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node: Node[K, V]) -> Node[K, V]:
        """nodeを根とする部分木を左回転させる

        Args:
            node (Node[K, V]): 回転させたい部分木の根
            parent (Optional[Node[K, V]]): nodeの親. Noneの場合はnodeが根であることを意味する

        Returns:
            Node[K, V]: 回転後の部分木の根

        Notes:
            nodeの右の子が存在することを前提とする
        """
        assert node.right

        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def search(self, key: K) -> Optional[Node[K, V]]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (K): 探索したい要素のkey

        Returns:
            Optional[Node[K, V]]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None

        node = self._splay(key, self.root, None)
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
        """二分探索木に要素を挿入する

        Args:
            key (K): 挿入したい要素のkey
            value (V): 挿入したい要素のvalue
        """
        if self.root is None:
            self.root = self._new_node(key, value)
            return

        # keyが存在する場合
        node = self.search(key)
        if node is not None:
            self.root.value = value
            return

        # keyが存在しない場合
        new_root = self._new_node(key, value)
        root = self.root
        if key < root.key:
            new_root.left, new_root.right = root.left, root
            root.left = None
        else:
            new_root.left, new_root.right = root, root.right
            root.right = None

        self.root = new_root

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

        node = self.search(key)

        # keyが存在しない場合
        if node is None:
            return default

        return_value = node.value
        # 子が0 or 1つの場合
        if node.left is None:
            self.root = node.right
            return return_value
        elif node.right is None:
            self.root = node.left
            return return_value
        # 子が2つの場合
        else:
            new_root = self._splay(node.left, key)
            new_root.right = node.right
            self.root = new_root
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

    def inorder(self) -> Generator[Node[K, V], None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[Node[K, V], None, None]: 二分探索木の中間順巡回で得られる要素
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

    def preorder(self) -> Generator[Node[K, V], None, None]:
        """二分探索木の先行順巡回 (二分探索木の要素を出力する)

        Yields:
            Generator[Node[K, V], None, None]: 二分探索木の先行順巡回で得られる要素
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
