#########################################################################################
# Splay Tree: 以下の操作を全て O(log N) で行う (Amortized).
# insert(key, value): key-value の挿入.
# delete(key): key-value の削除
# x in Splay: key xの存在判定.
# member(x): key x の存在判定.
# get(x): key x の value の取得.
# lower_bound(x): key x 以上のモノの中で最小のkeyを取得
# upper_bound(x): key x 未満のモノの中で最大のkeyを取得
# kth_elements(k): k番目の小さいkeyを返す（0-index）
# min_element(): 最小値を返す
# max_element(): 最大値を返す
#########################################################################################

#########################################################################################
# Verify
# ARC033 C - データ構造 (1058ms): https://atcoder.jp/contests/arc033/submissions/31062927
# 参考
# http://www.nct9.ne.jp/m_hiroi/light/pyalgo21.html#list2
#########################################################################################

#########################################################################################
# TODO
# mergeとsplit: https://www.ioi-jp.org/camp/2013/2013-sp-tasks/2013-sp-day4-spaceships-review.pdf
# kth-elementの高速化（splayしながら探索した方が早い）
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

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.size = 1

    def _fix_size(self):
        self.size = 1
        if self.left is not None:
            self.size += self.left.size
        if self.right is not None:
            self.size += self.right.size
        return

    def __repr__(self):
        return str(self.value)


class SplayTree:
    """Splay木: Top-Down Splay

    Attributes:
        root (Node): 根ノード. default to None
    """

    def __init__(self):
        self.root = None

    def _rotateL(self, u: Node):
        """uに対する左回転 (zig操作)

        Args:
            u (Node): 左回転を行う部分木

        Returns:
            Node: 左回転をした結果の部分木
        """
        v = u.right

        # sizeの修正
        v.size = u.size
        u.size -= (v.right.size + 1) if v.right is not None else 1

        # 繋ぎ変え
        u.right = v.left
        v.left = u
        return v

    def _rotateR(self, u: Node):
        """uに対する右1回転 (zig操作)

        Args:
            u (Node): 右回転を行う部分木

        Returns:
            Node: 右回転をした結果の部分木
        """
        v = u.left

        # sizeの修正
        v.size = u.size
        u.size -= (v.left.size + 1) if v.left is not None else 1

        # 繋ぎ変え
        u.left = v.right
        v.right = u
        return v

    def _fix_size(self, path):
        """splayを行ったあとの部分木のサイズの再計算

        Args:
            path (list): splay操作で辿ったパス
        """
        while path:
            node = path.pop()
            node._fix_size()
        return

    def _splay(self, key, node: Node = None):
        """splay操作

        Args:
            key (nay): 探索を行うkey
            node (Node, optional): splay操作をスタートするnode. Noneなら根から.
        """
        if node is None:
            node = self.root

        tmp_tree = Node(None, None)
        rnode = tmp_tree  # 右部分木になるnodeを追加する
        lnode = tmp_tree  # 左部分木になるnodeを追加する
        lpath, rpath = [], []  # size修正用のpath
        while True:
            if key == node.key:
                break
            elif key < node.key:  # 左に潜る
                if node.left is None:
                    break
                if key < node.left.key:  # zig-zig
                    node = self._rotateR(node)
                    if node.left is None:
                        break
                # 一時的な木に退避 & 現在のnodeの更新 & sizeの修正
                rnode.left = node
                lpath.append(node)
                rnode = node
                node = node.left
            else:  # 右に潜る
                if node.right is None:
                    break
                if node.right.key < key:  # zig-zig
                    node = self._rotateL(node)
                    if node.right is None:
                        break
                # 一時的な木に退避 & 現在のnodeの更新
                lnode.right = node
                rpath.append(node)
                lnode = node
                node = node.right

        # whileを抜けると, nodeには新しい根が入っている
        # nodeの子の繋ぎ変え
        rnode.left = node.right
        lnode.right = node.left
        node.left = tmp_tree.right
        node.right = tmp_tree.left

        # sizeの修正
        self._fix_size(lpath)
        self._fix_size(rpath)
        node._fix_size()
        return node

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

        # sizeの修正
        node._fix_size()
        insert_node._fix_size()

        self.root = insert_node
        return

    def delete(self, key):
        """keyの削除

        Args:
            key (any): 削除対象のキー

        Returns:
            any: 削除するkeyのvalue. 削除keyが存在しなければNone
        """
        if self.root is None:
            return None

        node = self._splay(key)

        # データが存在しない場合
        if node.key != key:
            self.root = node
            return None

        node_value = node.value
        # 存在する場合
        if node.left is None:
            self.root = node.right
        elif node.right is None:
            self.root = node.left
        else:
            # 削除nodeの左部分木の最大値ノードnode1
            node1 = self._splay(key, node=node.left)
            # node1は部分木の中で最大なので, 右の子を持たない
            node1.right = node.right
            self.root = node1

        if self.root is not None:
            self.root._fix_size()
        return node_value

    def member(self, key):
        """keyの存在判定

        Args:
            key (any): 存在判定するキー

        Returns:
            bool: keyが存在するかどうか
        """
        if self.root is None:
            return False

        node = self._splay(key)
        self.root = node
        return node.key == key

    def get(self, key):
        """keyのvalueを返す. keyが存在しなければ None を返す

        Args:
            key (nay): 検索対象のkey

        Returns:
            any: 指定したキーに付随するvalue. 存在しなければNone
        """
        if self.root is None:
            return None

        node = self._splay(key)
        self.root = node
        return node.value if node.key == key else None

    def lower_bound(self, key):
        """下限探索

        指定したkey以上のモノの中で, 最小のキーを見つける

        Args:
            key (any): キーの下限

        Returns:
            any: 条件を満たすキー. 存在しないならNone.
        """
        if self.root is None:
            return None

        node = self._splay(key)
        self.root = node

        # 右部分木の最小値を取得
        if node.key < key:
            if node.right is None:
                return None
            node = self._splay(key, node.right)
            self.root.right = node
        return node.key

    def upper_bound(self, key):
        """上限探索

        指定したkey"未満"のモノの中で, 最大のキーを見つける

        Args:
            key (any): キーの上限

        Returns:
            any: 条件を満たすキー. 存在しないならNone.
        """
        if self.root is None:
            return None

        node = self._splay(key)
        self.root = node

        # 左部分木の最大値を取得
        if key <= node.key:
            if node.left is None:
                return None
            node = self._splay(key, node.left)
            self.root.left = node
        return node.key

    def kth_element(self, k):
        """小さい方からk番目の要素を見つける

        Args:
            k (int): 何番目か (0-index)

        Note:
            要素がk未満なら, Noneを返す
            k番目の要素をsplayしてる

        Returns:
            any: 条件を満たすkey
        """
        if self.root is None:
            return None
        if self.root.size <= k:
            return None

        node = self.root
        s = 0
        while node is not None:
            if node.left is not None:
                t = s + node.left.size
            else:
                t = s

            # s + left < k なら 右の子へ, 違うなら左の子へ
            if t == k:
                break
            elif t < k:
                s = t + 1  # now node 分の +1
                node = node.right
            else:
                node = node.left

        node = self._splay(node.key)
        node._fix_size()
        self.root = node
        return self.root.key

    def min_element(self):
        """最小値を返す. 無いならNone"""
        return self.kth_element(0)

    def max_element(self):
        """最大値を返す. 無いならNone"""
        if self.root is None:
            return None
        max_k = self.root.size - 1
        return self.kth_element(max_k)

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

            print(f"parent = {now}, size = {now.size}")

            left = now.left
            right = now.right
            print(f"left = {left}, right = {right}")
            dfs(left)
            dfs(right)

        dfs(self.root)
        return ""


if __name__ == "__main__":
    import sys

    Q, *A = map(int, sys.stdin.buffer.read().split())
    splay = SplayTree()
    for t, x in zip(*[iter(A)] * 2):
        if t == 1:
            splay[x] = 1
        else:
            x = splay.kth_element(x - 1)
            del splay[x]
            print(x)
