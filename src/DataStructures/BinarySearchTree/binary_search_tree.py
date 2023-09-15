from typing import Optional, Generator
from collections import deque


class Node:
    """二分探索木のノード

    Attributes:
        key (int): 二分探索木のノードに格納される要素のkey
        left (Optional[Node]): 二分探索木のノードの左の子
        right (Optional[Node]): 二分探索木のノードの右の子
        count (int): このノードの個数 (多重集合の場合)
        subtree_size (int): このノードを根とする部分木の要素数

    Note:
        data(value)は載せてない
    """

    def __init__(self, key: int, count: int = 1):
        self.key = key
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.count = count
        self.subtree_size = count

    def _update(self):
        """このノードを根とする部分木の要素数を更新する
        """
        left_size = self.left.subtree_size if self.left is not None else 0
        right_size = self.right.subtree_size if self.right is not None else 0
        self.subtree_size = left_size + right_size + self.count

    def __repr__(self) -> str:
        return f"Node(key={self.key}, count={self.count})"


class BinarySearchTree:
    """基本的な二分探索木. 最悪計算時間は全てO(n)

    Attributes:
        root (Optional[Node]): 二分探索木の根

    Methods:
        search(key: int): 存在するならば二分探索木に要素k(key kを持つ要素)を返す
        count(key: int): 二分探索木に含まれるkeyの個数を返す
        insert(key: int, num: int): 二分探索木に要素k(key kを持つ要素)を挿入する
        delete(key: int, num: int): 二分探索木から要素k(key kを持つ要素)を削除する
        min_element(): 二分探索木の最小要素を返す
        max_element(): 二分探索木の最大要素を返す
        successor(key: int): key=kの次節点を返す
        predecessor(key: int): key=kの前節点を返す
        kth_smallest_element(k: int): 二分探索木の中間順巡回でk番目に小さい要素を返す
        kth_largest_element(k: int): 二分探索木の中間順巡回でk番目に大きい要素を返す
        inorder(): 二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)
        preorder(): 二分探索木の先行順巡回 (二分探索木の要素を出力する)
    """

    def __init__(self, A: list[int] = []):
        """初期化

        Args:
            A (list[T]): 初期化配列. Defaults to [].
        """
        self.root = None

        for a in A:
            self.insert(a)

    def __len__(self) -> int:
        """二分探索木の要素数を返す

        Returns:
            int: 二分探索木の要素数
        """
        return self.root.subtree_size if self.root is not None else 0

    def _new_node(self, key: int, count: int = 1) -> Node:
        return Node(key, count)

    def _update(self, path: list[Node]):
        """pathの各ノードの部分木の要素数を更新する

        Args:
            path (list[Node]): 更新したいノードのリスト. 根からのパスになっている必要がある
        """
        for node in reversed(path):
            node._update()

    def _search_with_path(self, key: int) -> list[Node]:
        """keyを持つ要素を二分探索木から探索する (探索パスを返す)

        Args:
            key (int): 探索したい要素のkey

        Returns:
            list[Node]: 探索パス
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

    def search(self, key: int) -> Optional[Node]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (int): 探索したい要素のkey

        Returns:
            Optional[Node]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None

        path = self._search_with_path(key)
        if path and path[-1].key != key:
            return None

        return path[-1]

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

        # keyが存在する場合
        if node.key == key:
            node.count += num
        # keyが存在しない場合
        else:
            parent = node
            if parent.key < key:
                parent.right = self._new_node(key, num)
            else:
                parent.left = self._new_node(key, num)

        self._update(path)

    def delete(self, key: int, num: int = 1):
        """二分探索木から要素を削除する

        Args:
            key (int): 削除したい要素のkey
            num (int): 削除したい要素の個数. Defaults to 1.
        """
        if self.root is None:
            return

        path = self._search_with_path(key)
        node = path[-1]
        parent = path[-2] if len(path) >= 2 else None

        # keyが存在しない場合
        if node.key != key:
            return

        node.count = max(0, node.count - num)

        # 削除しても要素が残る場合
        if node.count > 0:
            self._update(path)
            return

        # nodeが1つ以下の子を持つ場合
        if (node.left is None) or (node.right is None):
            child = node.left if node.left is not None else node.right
            # rootの場合
            if parent is None:
                self.root = child
            # parentの右の子の場合
            elif parent.key < key:
                parent.right = child
            # parentの左の子の場合
            else:
                parent.left = child

            # node自体は更新しなくて良い
            self._update(path[:-1])

            del node
            return

        # nodeが2つの子を持つ場合
        # nodeとnodeの次節点をswap -> nodeの削除
        successor_path = self._min_element_with_path(node.right)

        successor = successor_path[-1]
        successor_parent = successor_path[-2] if len(successor_path) >= 2 else node

        # successor_path = [R, ...., successor_parent, successor]
        if successor_parent.left is successor:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right

        successor.right = node.right
        successor.left = node.left

        if parent is None:
            self.root = successor
        elif parent.key < key:
            parent.right = successor
        else:
            parent.left = successor

        # root -> ... -> parent -> successor -> R -> ... -> successor_parentまでを更新
        self._update(path[:-1] + [successor] + successor_path[:-1])

        del node

    def _min_element_with_path(self, root: Node) -> list[Node]:
        """rootを根とする部分木の最小要素を返す (探索パスを返す)

        Args:
            root (Node): 根

        Returns:
            list[Node]: 最小要素に至る探索パス
        """
        path = []
        node = root
        while node is not None:
            path.append(node)
            node = node.left
        return path

    def min_element(self) -> Optional[Node]:
        """二分探索木の最小要素を返す

        Returns:
            Optional[Node]: 二分探索木の最小要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._min_element_with_path(self.root)[-1]

    def _max_element_with_path(self, root: Node) -> list[Node]:
        """rootを根とする部分木の最大要素を返す (探索パスを返す)

        Args:
            root (Node): 根

        Returns:
            list[Node]: 最大要素に至る探索パス
        """
        path = []
        node = root
        while node is not None:
            path.append(node)
            node = node.right
        return path

    def max_element(self) -> Optional[Node]:
        """二分探索木の最大要素を返す

        Returns:
            Optional[Node]: 二分探索木の最大要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._max_element_with_path(self.root)[-1]

    def successor(self, key: int) -> Optional[Node]:
        """keyの次節点を返す

        Args:
            key (int): 検索したいkey

        Returns:
            Optional[Node]: key < x となる最小の要素x. keyが存在しない場合 or keyの次節点が存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            return None

        # 右の子が存在する場合
        if node.right is not None:
            return self._min_element_with_path(node.right)[-1]

        # root = key ^ 右の子が存在しない場合
        if len(path) == 1:
            return None

        path = path[::-1]
        # nodeがparentの左の子である場合 -> parentがnodeの次節点
        for node, parent in zip(path, path[1:]):
            if parent.left is node:
                return parent

        return None

    def predecessor(self, key: int) -> Optional[Node]:
        """keyの前節点を返す

        Args:
            key (int): 検索したいkey

        Returns:
            Optional[Node]: key > x となる最大の要素x. keyが存在しない場合 or keyの前節点が存在しない場合はNoneを返す
        """
        if self.root is None:
            return None

        path = self._search_with_path(key)
        node = path[-1]

        # keyが存在しない場合
        if node.key != key:
            return None

        # 左の子が存在する場合は左の子の最大要素が前節点
        if node.left is not None:
            return self._max_element_with_path(node.left)[-1]

        # root = key ^ 左の子が存在しない場合
        if len(path) == 1:
            return None

        path = path[::-1]
        # nodeがparentの右の子である場合 -> parentがnodeの前節点
        for node, parent in zip(path, path[1:]):
            if parent.right is node:
                return parent

        return None

    def kth_smallest_element(self, k: int) -> Optional[Node]:
        """二分探索木の中間順巡回でk番目に小さい要素を返す

        Args:
            k (int): k番目に小さい要素 (kは1-indexed)

        Returns:
            Optional[Node]: 二分探索木の中間順巡回でk番目に小さい要素. 存在しない場合はNoneを返す
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

    def kth_largest_element(self, k: int) -> Optional[Node]:
        """二分探索木の中間順巡回でk番目に大きい要素を返す

        Args:
            k (int): k番目に大きい要素 (kは1-indexed)

        Returns:
            Optional[Node]: 二分探索木の中間順巡回でk番目に大きい要素. 存在しない場合はNoneを返す
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

    def inorder(self) -> Generator[Node, None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[Node, None, None]: 二分探索木の中間順巡回で得られる要素
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

    def preorder(self) -> Generator[Node, None, None]:
        """二分探索木の先行順巡回 (二分探索木の要素を出力する)

        Yields:
            Generator[Node, None, None]: 二分探索木の先行順巡回で得られる要素
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
