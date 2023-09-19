# TODO: 実装
# TODO: Merge, Split, Queryの追加

from typing import Optional, Generator
from collections import deque


class ScapegoatNode:
    """ScapegoatTreeのノード

    Attributes:
        key (int): 二分探索木のノードに格納される要素のkey
        left (Optional[ScapegoatNode]): 二分探索木のノードの左の子
        right (Optional[ScapegoatNode]): 二分探索木のノードの右の子
        subtree_size (int): このノードを根とする部分木の要素数
        removed (bool): このノードが削除されているかどうか

    Note:
        data(value)は載せてない
        多重集合化はしていない
    """

    def __init__(self, key: int, count: int = 1):
        self.key = key
        self.left: Optional[ScapegoatNode] = None
        self.right: Optional[ScapegoatNode] = None
        self.subtree_size = count
        self.removed = False

    def _update(self):
        """このノードを根とする部分木の要素数を更新する
        """
        left_size = self.left.subtree_size if self.left is not None else 0
        right_size = self.right.subtree_size if self.right is not None else 0
        self.subtree_size = left_size + right_size

        if self.removed is False:
            self.subtree_size += 1

    def __repr__(self) -> str:
        return f"Node(key={self.key}, count={self.count})"


class ScapeGoatTree:
    """ScapeGoatTree. 計算量は Amortized O(logN)

    Attributes:
        root (Optional[ScapegoatNode]): 二分探索木の根

    Methods:
        search(key: int): 存在するならば二分探索木に要素k(key kを持つ要素)を返す
        count(key: int): 二分探索木に含まれるkeyの個数を返す
        insert(key: int, num: int): 二分探索木に要素k(key kを持つ要素)を挿入する
        delete(key: int, num: int): 二分探索木から要素k(key kを持つ要素)を削除する
        min_element(): 二分探索木の最小要素を返す
        max_element(): 二分探索木の最大要素を返す
        successor(key: int): key=kの次節点を返す
        predecessor(key: int): key=kの前節点を返す
        lower_bound(key: int): key <= x.key となる最小のxを返す
        upper_bound(key: int): x.key <= key となる最大のxを返す
        kth_smallest_element(k: int): 二分探索木の中間順巡回でk番目に小さい要素を返す
        kth_largest_element(k: int): 二分探索木の中間順巡回でk番目に大きい要素を返す
        inorder(): 二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)
        preorder(): 二分探索木の先行順巡回 (二分探索木の要素を出力する)
    """

    def __init__(self):
        """初期化
        """
        self.root = None
        self.alpha = 0.7

    def __len__(self) -> int:
        """二分探索木の要素数を返す

        Returns:
            int: 二分探索木の要素数
        """
        return self.root.subtree_size if self.root is not None else 0

    def _new_node(self, key: int, count: int = 1) -> ScapegoatNode:
        return ScapegoatNode(key, count)

    def _update(self, path: list[ScapegoatNode]):
        """pathの各ノードの部分木の要素数を更新する

        Args:
            path (list[ScapegoatNode]): 更新したいノードのリスト. 根からのパスになっている必要がある
        """
        for node in reversed(path):
            node._update()

    def _search_with_path(self, key: int) -> list[ScapegoatNode]:
        """keyを持つ要素を二分探索木から探索する (探索パスを返す)

        Args:
            key (int): 探索したい要素のkey

        Returns:
            list[ScapegoatNode]: 探索パス
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

    def search(self, key: int) -> Optional[ScapegoatNode]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (int): 探索したい要素のkey

        Returns:
            Optional[ScapegoatNode]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        if self.root is None:
            return None

        path = self._search_with_path(key)
        if path and path[-1].key != key:
            return None

        return path[-1]

    def _inorder(self, root: ScapegoatNode) -> Generator[ScapegoatNode, None, None]:
        """rootを根とする部分木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Args:
            root (ScapegoatNode): 根

        Yields:
            Generator[ScapegoatNode, None, None]: rootを根とする部分木の中間順巡回で得られる要素
        """
        dq = deque([[root, False]])
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

    def _rebuild_recursion(self, nodes: list[ScapegoatNode]) -> Optional[ScapegoatNode]:
        if len(nodes) == 0:
            return None

        if len(nodes) == 1:
            node = nodes[0]
            node.left = None
            node.right = None
            node._update()
            return node

        mid = len(nodes) // 2
        root = nodes[mid]
        root.left = self._rebuild_recursion(nodes[:mid])
        root.right = self._rebuild_recursion(nodes[mid + 1:])
        root._update()
        return root

    def _rebuild(self, scapegoat: ScapegoatNode, parent: Optional[ScapegoatNode]) -> ScapegoatNode:
        """scapegoatを根とする部分木を再構築する

        Args:
            scapegoat (ScapegoatNode): 再構築したい部分木の根
            parent (Optional[ScapegoatNode]): scapegoatの親

        Returns:
            ScapegoatNode: 再構築した部分木の根
        """
        nodes = [node for node in self._inorder(scapegoat) if node.count > 0]
        new_root = self._rebuild_recursion(nodes)

        if parent is None:
            self.root = new_root
        elif parent.key < scapegoat.key:
            parent.right = new_root
        else:
            parent.left = new_root

        return new_root

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

        scapegoat = None
        for node in reversed(path):

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

    def _min_element_with_path(self, root: ScapegoatNode) -> list[ScapegoatNode]:
        """rootを根とする部分木の最小要素を返す (探索パスを返す)

        Args:
            root (ScapegoatNode): 根

        Returns:
            list[ScapegoatNode]: 最小要素に至る探索パス
        """
        path = []
        node = root
        while node is not None:
            path.append(node)
            node = node.left
        return path

    def min_element(self) -> Optional[ScapegoatNode]:
        """二分探索木の最小要素を返す

        Returns:
            Optional[ScapegoatNode]: 二分探索木の最小要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._min_element_with_path(self.root)[-1]

    def _max_element_with_path(self, root: ScapegoatNode) -> list[ScapegoatNode]:
        """rootを根とする部分木の最大要素を返す (探索パスを返す)

        Args:
            root (ScapegoatNode): 根

        Returns:
            list[ScapegoatNode]: 最大要素に至る探索パス
        """
        path = []
        node = root
        while node is not None:
            path.append(node)
            node = node.right
        return path

    def max_element(self) -> Optional[ScapegoatNode]:
        """二分探索木の最大要素を返す

        Returns:
            Optional[ScapegoatNode]: 二分探索木の最大要素. 二分探索木が空ならばNoneを返す
        """
        if self.root is None:
            return None
        return self._max_element_with_path(self.root)[-1]

    def successor(self, key: int) -> Optional[ScapegoatNode]:
        """keyの次節点を返す

        Args:
            key (int): 検索したいkey

        Returns:
            Optional[ScapegoatNode]: key < x となる最小の要素x. keyが存在しない場合 or keyの次節点が存在しない場合はNoneを返す
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

    def predecessor(self, key: int) -> Optional[ScapegoatNode]:
        """keyの前節点を返す

        Args:
            key (int): 検索したいkey

        Returns:
            Optional[ScapegoatNode]: key > x となる最大の要素x. keyが存在しない場合 or keyの前節点が存在しない場合はNoneを返す
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

    def lower_bound(self, key: int) -> Optional[ScapegoatNode]:
        """key <= x.key となる最小のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[ScapegoatNode]: key <= x.key となる最小のx. 存在しない場合はNoneを返す
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

    def upper_bound(self, key: int) -> Optional[ScapegoatNode]:
        """x.key <= keyとなる最大のxを返す

        Args:
            key (int): lower

        Returns:
            Optional[ScapegoatNode]: x.key <= keyとなる最大のx. 存在しない場合はNoneを返す
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

    def kth_smallest_element(self, k: int) -> Optional[ScapegoatNode]:
        """二分探索木の中間順巡回でk番目に小さい要素を返す

        Args:
            k (int): k番目に小さい要素 (kは1-indexed)

        Returns:
            Optional[ScapegoatNode]: 二分探索木の中間順巡回でk番目に小さい要素. 存在しない場合はNoneを返す
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

    def kth_largest_element(self, k: int) -> Optional[ScapegoatNode]:
        """二分探索木の中間順巡回でk番目に大きい要素を返す

        Args:
            k (int): k番目に大きい要素 (kは1-indexed)

        Returns:
            Optional[ScapegoatNode]: 二分探索木の中間順巡回でk番目に大きい要素. 存在しない場合はNoneを返す
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

    def inorder(self) -> Generator[ScapegoatNode, None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[ScapegoatNode, None, None]: 二分探索木の中間順巡回で得られる要素
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

    def preorder(self) -> Generator[ScapegoatNode, None, None]:
        """二分探索木の先行順巡回 (二分探索木の要素を出力する)

        Yields:
            Generator[ScapegoatNode, None, None]: 二分探索木の先行順巡回で得られる要素
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
