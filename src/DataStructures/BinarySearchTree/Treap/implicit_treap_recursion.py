from typing import Optional, Generator, Generic, TypeVar, Callable
from collections import deque
from random import random


Value = TypeVar("Value")


class TreapNode(Generic[Value]):
    """Treapのノード

    Args:
        Value: 二分探索木に格納する値の型

    Attributes:
        value (Value): 配列上のindexに格納される値
        left (Optional[TreapNode[Value]]): 二分探索木のノードの左の子
        right (Optional[TreapNode[Value]]): 二分探索木のノードの右の子
        subtree_size (int): このノードを根とする部分木の要素数
        priority (float): このノードの優先度
        aggregation_value (Value): このノードを根とする部分木の集約値
    """

    def __init__(self, value: Value):
        self.value = value
        self.left: Optional[TreapNode[Value]] = None
        self.right: Optional[TreapNode[Value]] = None
        self.subtree_size = 1
        self.priority = random()
        self.aggregation_value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def _debug(self) -> str:
        return f"Node{self.value=}, {self.left=}, {self.right=}, {self.subtree_size=}, {self.aggregation_value=}"


class ImplicitTreap(Generic[Value]):
    """ImplicitTreap. Treapを配列のように扱う. (再帰)

    Args:
        Value: 二分探索木に格納する値の型

    Attributes:
        root (Optional[TreapNode[Value]]): 二分探索木の根
        aggregate_func (Callable[[Value, Value], Value]): 集約関数 (例: min, max, add)
        add_func (Callable[[Value, Value], Value]): 加算関数

    Methods:
        __len__(): 要素数を返す
        __contains__(v: Value): vが含まれているかを返す, これだけO(N)かかるので注意
        __getitem__(i: int): i番目の要素を返す
        __setitem__(i: int, v: Value): i番目の要素をvに更新する
        update(i: int, v: Value): i番目の要素をvに更新する
        add(i: int, v: Value): i番目の要素にvを加算する (add_funcを使う)
        append(v: Value): 末尾にvを追加する
        insert(i: int, v: Value): i番目にvを挿入する
        pop(i: int): i番目の要素を削除してその要素を返す
        query(i: int, j: int): [i..j)の集約値を返す
        search(key: int): 存在するならば二分探索木に要素k(key kを持つ要素)を返す

    Notes:
        ヒープ条件: 親のpriority >= 子のpriority
    """

    def __init__(
        self,
        aggregate_func: Callable[[Value, Value], Value],
        add_func: Callable[[Value, Value], Value]
    ):
        """初期化
        """
        self.root: Optional[TreapNode[Value]] = None
        self.aggregate_func = aggregate_func
        self.add_func = add_func

    def _node_update(self, node: Optional[TreapNode[Value]]):
        """nodeの情報を更新する

        Args:
            node (Optional[TreapNode[Value]]): 更新したいノード
        """
        if node is None:
            return
        elif node.left is None and node.right is None:
            node.subtree_size = 1
            node.aggregation_value = node.value
            return
        elif node.left is None:
            node.subtree_size = node.right.subtree_size + 1
            node.aggregation_value = self.aggregate_func(node.value, node.right.aggregation_value)
            return
        elif node.right is None:
            node.subtree_size = node.left.subtree_size + 1
            node.aggregation_value = self.aggregate_func(node.left.aggregation_value, node.value)
            return
        else:
            node.subtree_size = node.left.subtree_size + node.right.subtree_size + 1
            aggregation_value = self.aggregate_func(
                node.left.aggregation_value,
                node.value
            )
            aggregation_value = self.aggregate_func(
                aggregation_value,
                node.right.aggregation_value
            )
            node.aggregation_value = aggregation_value
            return

    def _new_node(self, value: Value) -> TreapNode[Value]:
        return TreapNode[Value](value)

    def _merge(
        self,
        left: Optional[TreapNode[Value]],
        right: Optional[TreapNode[Value]]
    ) -> Optional[TreapNode[Value]]:
        """leftを根とする部分木と, rightを根とする部分木をマージする

        Args:
            left (Optional[TreapNode[Value]]): leftの根
            right (Optional[TreapNode[Value]]): rightの根

        Returns:
            Optional[TreapNode[Value]]: mergeした後の根
        """
        if (left is None) and (right is None):
            return None
        if left is None:
            return right
        if right is None:
            return left

        if left.priority < right.priority:
            right.left = self._merge(left, right.left)
            self._node_update(right)
            return right
        else:
            left.right = self._merge(left.right, right)
            self._node_update(left)
            return left

    def _split(
        self,
        root: Optional[TreapNode[Value]],
        key: int
    ) -> tuple[Optional[TreapNode[Value]], Optional[TreapNode[Value]]]:
        """key未満のkeyからなるTreapと, key以上のkeyからなるTreapに分割する

        Args:
            root (Optional[TreapNode[Value]]): 分割したい部分木の根
            key (int): 分割するkey

        Returns:
            tuple[Optional[TreapNode[Value]], Optional[TreapNode[Value]]]: 分割した後の根
        """
        if root is None:
            return None, None

        # rootの配列上の番号
        implicit_key = (root.left.subtree_size if root.left is not None else 0) + 1

        # (root.left + root)が左, root.rightが右
        if implicit_key == key:
            right = root.right
            root.right = None
            self._node_update(root)
            return root, right

        # root.leftを分割
        elif key < implicit_key:
            left, right = self._split(root.left, key)
            root.left = right
            self._node_update(root)
            return left, root

        # root.rightを分割
        else:
            left, right = self._split(root.right, key - implicit_key)
            root.right = left
            self._node_update(root)
            return root, right

    def search(self, key: int) -> Optional[TreapNode[Value]]:
        """keyを持つ要素を二分探索木から探索する

        Args:
            key (int): 探索したい要素のkey

        Returns:
            Optional[TreapNode[Value]]: keyを持つ要素が存在すればその要素を返す. 存在しなければNoneを返す
        """
        # [0..key+1), [key+1..n)
        left, right = self._split(self.root, key + 1)
        # [0..key), [key..key+1)
        left, mid = self._split(left, key)

        root = self._merge(left, mid)
        root = self._merge(root, right)
        return mid

    def insert(self, i: int, value: Value):
        """i番目にvalueを挿入する

        Args:
            i (int): 挿入したい要素のindex
            value (Value): 挿入したい要素の値
        """
        # [0..i), [i..n)
        left, right = self._split(i)
        node = self._new_node(value)

        # 元に戻す
        root = self._merge(left, node)
        root = self._merge(root, right)
        self.root = root

    def append(self, value: Value):
        """末尾にvalueを追加する

        Args:
            value (Value): 追加したい要素の値
        """
        node = self._new_node(value)
        root = self._merge(self.root, node)
        self.root = root

    def pop(self, i: int = -1) -> Value:
        """i番目の要素を削除してその要素を返す

        Args:
            i (int): 削除したい要素のindex, デフォルトは末尾

        Raises:
            IndexError: iが範囲外の場合

        Returns:
            Value: 削除した要素
        """
        if i == -1:
            i = len(self) - 1

        if (self.root is None) or not (0 <= i < len(self)):
            raise IndexError("list index out of range")

        # [0..i + 1), [i + 1..n)
        left, right = self._split(self.root, i + 1)
        # [0..i), [i..i + 1)
        left, mid = self._split(left, i)

        # 元に戻す
        root = self._merge(left, right)
        self.root = root
        return mid.value

    def query(self, i: int, j: int) -> Value:
        """[i..j)の集約値を返す

        Args:
            i (int): 集約したい区間の左端
            j (int): 集約したい区間の右端

        Returns:
            Value: [i..j)の集約値
        """
        # [0..j), [j..n)
        left, right = self._split(self.root, j)
        # [0..i), [i..j)
        left, mid = self._split(left, i)

        return_value = mid.aggregation_value

        root = self._merge(left, mid)
        root = self._merge(root, right)
        self.root = root
        return return_value

    def update(self, i: int, value: Value):
        """i番目の要素をvalueに更新する

        Args:
            i (int): 更新したい要素のindex
            value (Value): 更新したい要素の値

        Raises:
            IndexError: iが範囲外の場合
        """
        if (self.root is None) or not (0 <= i < len(self)):
            raise IndexError("list index out of range")

        # [0..i+1), [i+1..n)
        left, right = self._split(self.root, i + 1)
        # [0..i), [i..i+1)
        left, mid = self._split(left, i)

        # 更新
        mid.value = value
        self._node_update(mid)

        # 元に戻す
        root = self._merge(left, mid)
        root = self._merge(root, right)

    def add(self, i: int, value: Value):
        """i番目の要素をvalueを加算する (add_funcを使う)

        Args:
            i (int): 更新したい要素のindex
            value (Value): 加算値

        Raises:
            IndexError: iが範囲外の場合
        """

        if (self.root is None) or not (0 <= i < len(self)):
            raise IndexError("list index out of range")

        # [0..i+1), [i+1..n)
        left, right = self._split(self.root, i + 1)
        # [0..i), [i..i+1)
        left, mid = self._split(left, i)

        # 更新
        mid.value = self.add_func(mid.value, value)
        self._node_update(mid)

        # 元に戻す
        root = self._merge(left, mid)
        root = self._merge(root, right)

    def __len__(self) -> int:
        """二分探索木の要素数を返す

        Returns:
            int: 二分探索木の要素数
        """
        return self.root.subtree_size if self.root is not None else 0

    def __getitem__(self, i: int) -> Value:
        """i番目の要素を返す

        Args:
            i (int): 取得したい要素のindex

        Raises:
            IndexError: iが範囲外の場合

        Returns:
            Value: i番目の要素
        """
        if (self.root is None) or not (0 <= i < len(self)):
            raise IndexError("list index out of range")
        node = self.search(i)
        return node.value

    def __setitem__(self, i: int, value: Value):
        self.update(i, value)

    def __contains__(self, value: Value) -> bool:
        """valueが二分探索木に含まれているかどうかを返す

        Args:
            value (Value): 二分探索木に含まれているかどうかを調べたい要素のvalue

        Returns:
            bool: valueが二分探索木に含まれているかどうか
        """
        for node in self._inorder():
            if node.value == value:
                return True
        return False

    def __iter__(self):
        return self._inorder()

    def _inorder(self) -> Generator[TreapNode[Value], None, None]:
        """二分探索木の中間順巡回 (二分探索木の要素を昇順に出力する)

        Yields:
            Generator[TreapNode[Value], None, None]: 二分探索木の中間順巡回で得られる要素
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


def RangeMinimumQuery(A: list[int]) -> ImplicitTreap[int]:
    """RangeMinimumQueryを行うTreapを返す

    Args:
        A (list[int]): RangeMinimumQueryを行いたい配列

    Returns:
        ImplicitTreap[int]: RangeMinimumQueryを行うTreap
    """
    treap = ImplicitTreap[int](min, lambda x, y: x + y)
    for a in A:
        treap.append(a)
    return treap


def RangeSumQuery(A: list[int]) -> ImplicitTreap[int]:
    """RangeSumQueryを行うTreapを返す

    Args:
        A (list[int]): RangeSumQueryを行いたい配列

    Returns:
        ImplicitTreap[int]: RangeSumQueryを行うTreap
    """
    treap = ImplicitTreap[int](
        lambda x, y: x + y,
        lambda x, y: x + y
    )

    for a in A:
        treap.append(a)

    return treap


def RangeCompositeQuery(A: list[tuple[int, int]]) -> ImplicitTreap[tuple[int, int]]:
    """RangeCompositeQueryを行うTreapを返す

    Args:
        A (list[tuple[int, int]]): RangeCompositeQueryを行いたい配列

    Returns:
        ImplicitTreap[tuple[int, int]]: RangeCompositeQueryを行うTreap

    Notes:
        A[i] = [a, b] -> f_i(x) = ax + b
        query(left, right) = f_{right-1}(f_{right-2}..(...f_{left}(x)))
        MOD付き
    """
    MOD = 998244353

    # Addは無し
    treap = ImplicitTreap[tuple[int, int]](
        lambda x, y: [(y[0] * x[0]) % MOD, (y[0] * x[1] + y[1]) % MOD],
        lambda x, y: x + y
    )

    for a in A:
        treap.append(a)

    return treap
