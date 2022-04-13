#########################################################################################
# 赤黒木: 以下の操作を全て O(log N) で行う
#########################################################################################

#########################################################################################
# Verify
# 参考
# http://www.nct9.ne.jp/m_hiroi/light/pyalgo21.html#list2
#########################################################################################

#########################################################################################
# TODO
#########################################################################################


class Node:
    """Splay木の各データを表すノード

    Attributes:
        key (any): ノードのキー. 比較可能である必要がある.
        value (any): ノードの値 (保存したいデータ)
        left (Node): 左の子ノード
        right (Node): 右の子ノード
        size (int): 部分木のサイズ（自分を含む）
    """

    def __init__(self, key, value, color=1):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.size = 1

    def __repr__(self):
        return str(self.value)


class SplayTree:
    """Splay木: Top-Down Splay

    Attributes:
        root (Node): 根ノード. default to None
    """

    def __init__(self):
        self.root = None

    def _zig(self, u: Node):
        pass

    def _zig_zig(self, u: Node):
        pass

    def _zig_zag(self, u: Node):
        pass

    def _splay(self, key):
        """key が 新しくnodeに来るデータ
        Args:
            x (_type_): _description_
        """
        tmp_tree = Node(None, None)
        r_node = tmp_tree.right
        l_node = tmp_tree.left

        while True:

        pass

    def _search(self, key):
        """対象のkeyの場所までのpathを探索する

        Args:
            key (any): 探索対象のkey
        """
        now = self.root
        path = []
        while now is not None:
            if key < now.key:  # 左の子へ進む
                path.append((now, 1))
                now = now.left
            elif now.key < key:  # 右の子へ進む
                path.append((now, -1))
                now = now.right
            elif now.key == key:  # 終了
                path.append((now, 0))
                break
        return path

    def insert(self, key, value=None):
        """値の挿入

        Args:
            key (any): データのkey
            value (any): keyに対応するデータ

        Note:
            同じkeyが存在する場合, valueを上書きする
            defaultでは, key=value としている
        """
        if value is None:
            value = key

        # 空のsplay木だったら, 根に追加
        if self.root is None:
            self.root = Node(key, value)
            return

        # serchはsplay操作を行ってるので, 根ノードが帰ってくる
        node = self._splay(key)

        # Splay Treeに同じkeyの要素があったら, 根ノードの変更のみ
        if node.key == key:
            node.value = value
            self.root = node
            return

        # そうでないなら, 新しく挿入するノードを根にする
        insert_node = Node(key, value)
        if key < node.key:
            # new_rootはkey以上のmin
            # -> new_root.left < x
            insert_node.right = node
            insert_node.left = node.left
            node.left = None
        else:
            # new_rootはkey未満のmax
            # -> x < new_root.right
            insert_node.left = node
            insert_node.right = node.right
            node.right = None
        self.root = insert_node
        return

    def delete(self, key):
        pass

    def member(self, key):
        pass

    def get(self, key):
        pass

    def lower_bound(self, key):
        pass

    def upper_bound(self, key):
        pass

    def kth_element(self, k):
        pass

    def __contains__(self, key):
        return self.get(key)

    def __len__(self):
        return self.root.size if self.root is not None else 0

    def __bool__(self):
        return self.root is not None

    def __getitem__(self, key):
        # list[1] の ような要素の取得の特殊メソッド
        return self.get(key)

    def __setitem__(self, key, value):
        # list[1] = 2 の ような要素のセットの特殊メソッド
        return self.insert(key, value)

    def __delitem__(self, key):
        # del文で呼び出されるメソッド
        return self.delete(key)

    def __repr__(self):

        def dfs(now):
            if now is None:
                return ""

            print(f"parent = {now}")
            print(f"bias = {now.bias}, size = {now.size}")

            left = now.left
            right = now.right
            print(f"left = {left}, right = {right}")
            dfs(left)
            dfs(right)

        dfs(self.root)
        return ""
