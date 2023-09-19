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
        subtree_size (int): このノードを根とする部分木の要素数
    """

    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.subtree_size = 1

    def _update(self):
        """このノードを根とする部分木の要素数を更新する
        """
        left_size = self.left.subtree_size if self.left is not None else 0
        right_size = self.right.subtree_size if self.right is not None else 0
        self.subtree_size = left_size + right_size + 1

    def __repr__(self) -> str:
        return f"Node(key={self.key}, value={self.value})"


class SplayHashMap(Generic[K, V]):
    """BottomUp Splay Tree (非再帰)を用いたHashMap

    Args:
        K: 二分探索木のノードに格納される要素のkeyの型 (比較可能である必要がある)
        V: 二分探索木のノードに格納される要素のvalueの型

    Attributes:
        root (Optional[Node[K, V]]): 二分探索木の根

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

    def _new_node(self, key: K, value: V) -> Node[K, V]:
        return Node(key, value)

    def _search_with_path(self, key: K) -> list[tuple[Node[K, V], int]]:
        """keyを持つ要素を二分探索木から探索する (探索パスを返す)

        Args:
            key (K): 探索したい要素のkey

        Returns:
            list[tuple[Node[K, V], int]]: 探索パス(node, nodeから移動した方向), 方向は 0->左, 1->右, -1->終了.
        """
        if self.root is None:
            return []

        node = self.root
        path = []
        while node is not None:
            if node.key == key:
                path.append((node, -1))
                break

            if node.key < key:
                path.append((node, 1))
                node = node.right
            else:
                path.append((node, 0))
                node = node.left
        return path

    def _rotate_right(self, node: Node[K, V], parent: Optional[Node[K, V]]) -> Node[K, V]:
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

        if parent is None:
            self.root = new_root
        elif parent.key < node.key:
            parent.right = new_root
        else:
            parent.left = new_root

        node._update()
        new_root._update()
        return new_root

    def _rotate_left(self, node: Node[K, V], parent: Optional[Node[K, V]]) -> Node[K, V]:
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

        if parent is None:
            self.root = new_root
        elif parent.key < node.key:
            parent.right = new_root
        else:
            parent.left = new_root

        node._update()
        new_root._update()
        return new_root

    def _splay(
        self,
        path: list[tuple[Node[K, V], int]],
        root_parent: Optional[Node[K, V]] = None
    ) -> Optional[Node[K, V]]:
        """pathの最後のノードを根に持ってくる (BottomUpSplay)

        Args:
            path (list[tuple[Node[K, V], int]]): root->...->target_nodeのpath(node, nodeから移動した方向)
            root_parent (Optional[Node[K, V]]): rootの親. Noneの場合はrootが根であることを意味する

        Returns:
            Optional[Node[K, V]]: 根に持ってきたノード

        Notes:
            rootはSplayTreeのrootでなくても良い (部分木でも良い)
        """
        if path == []:
            return

        target_node, _ = path.pop()
        while len(path) > 1:
            node, node_dir = path.pop()
            parent, parent_dir = path.pop()
            # zig-zig
            if node_dir == parent_dir:
                if node_dir == 0:
                    self._rotate_right(parent, path[-1][0] if path else None)
                    self._rotate_right(node, path[-1][0] if path else None)
                else:
                    self._rotate_left(parent, path[-1][0] if path else None)
                    self._rotate_left(node, path[-1][0] if path else None)
            # zig-zag
            else:
                if node_dir == 0:
                    self._rotate_right(node, parent)
                    self._rotate_left(parent, path[-1][0] if path else None)
                else:
                    self._rotate_left(node, parent)
                    self._rotate_right(parent, path[-1][0] if path else None)

        if len(path) == 0:
            return target_node

        node, node_dir = path.pop()
        if node_dir == 0:
            self._rotate_right(node, root_parent)
        else:
            self._rotate_left(node, root_parent)

        return target_node

    def search(self, key: K) -> Optional[Node[K, V]]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (K): 探索したい要素のkey

        Returns:
            Optional[Node[K, V]]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None

        path = self._search_with_path(key)
        node = self._splay(path)
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
            self.root._update()
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

        root._update()
        new_root._update()
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
            path = self._max_element_with_path(node.left)
            new_root = self._splay(path, node)
            new_root.right = node.right
            new_root._update()
            self.root = new_root
            return return_value

    def delete(self, key: K):
        """二分探索木から要素を削除する

        Args:
            key (K): 削除したい要素のkey
        """
        self.pop(key)

    def _min_element_with_path(self, root: Node[K, V]) -> list[tuple[Node[K, V], int]]:
        """rootを根とする部分木の最小要素を返す (探索パスを返す)

        Args:
            root (Node[K, V]): 根

        Returns:
            list[Node[K, V]]: 最小要素に至る探索パス(node, nodeから移動した方向), 方向は 0->左, 1->右, -1->終了.
        """
        path = []
        node = root
        while node is not None:
            path.append((node, 0))
            node = node.left
        return path

    def min_element(self) -> Optional[Node[K, V]]:
        """二分探索木の最小要素を返す

        Returns:
            Optional[Node[K, V]]: 二分探索木の最小key要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        path = self._min_element_with_path(self.root)
        self._splay(path)
        return self.root

    def _max_element_with_path(self, root: Node[K, V]) -> list[tuple[Node[K, V], int]]:
        """rootを根とする部分木の最大要素を返す (探索パスを返す)

        Args:
            root (Node[K, V]): 根

        Returns:
            list[Node[K, V]]: 最大要素に至る探索パス(node, nodeから移動した方向), 方向は 0->左, 1->右, -1->終了.
        """
        path = []
        node = root
        while node is not None:
            path.append((node, 1))
            node = node.right
        return path

    def max_element(self) -> Optional[Node[K, V]]:
        """二分探索木の最大要素を返す

        Returns:
            Optional[Node[K, V]]: 二分探索木の最大key要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        path = self._max_element_with_path(self.root)
        self._splay(path)
        return self.root

    def lower_bound(self, key: K) -> Optional[Node[K, V]]:
        """key <= x.key となる最小のxを返す

        Args:
            key (K): lower

        Returns:
            Optional[Node[K, V]]: key <= x.key となる最小のx. 存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        self.search(key)

        node = self.root
        # 右部分木の最小値
        if node.key < key:
            path = self._min_element_with_path(node.right)
            self._splay(path, node)
            node = node.right

        return node

    def upper_bound(self, key: K) -> Optional[Node[K, V]]:
        """x.key <= keyとなる最大のxを返す

        Args:
            key (K): lower

        Returns:
            Optional[Node[K, V]]: x.key <= keyとなる最大のx. 存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        self.search(key)

        node = self.root
        # 左部分木の最大値
        if key < node.key:
            path = self._max_element_with_path(node.left)
            self._splay(path, node)
            node = node.left

        return node

    def kth_smallest_element(self, k: int) -> Optional[Node[K, V]]:
        """二分探索木の中間順巡回でk番目に小さい要素を返す

        Args:
            k (int): k番目に小さい要素 (kは1-indexed)

        Returns:
            Optional[Node[K, V]]: 二分探索木の中間順巡回でk番目に小さい要素. 存在しない場合はNoneを返す
        """
        if len(self) < k:
            return None

        path = []
        node = self.root
        while node is not None:
            left = node.left.subtree_size if node.left is not None else 0
            # そのnodeに含まれる場合
            if left < k <= left + node.count:
                path.append((node, -1))
                break

            # 左に含まれる場合
            if k <= left:
                path.append((node, 0))
                node = node.left
            # 右に含まれる場合
            else:
                k -= (left + node.count)
                path.append((node, 1))
                node = node.right

        self._splay(path)
        return self.root

    def kth_largest_element(self, k: int) -> Optional[Node[K, V]]:
        """二分探索木の中間順巡回でk番目に大きい要素を返す

        Args:
            k (int): k番目に大きい要素 (kは1-indexed)

        Returns:
            Optional[Node[K, V]]: 二分探索木の中間順巡回でk番目に大きい要素. 存在しない場合はNoneを返す
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
