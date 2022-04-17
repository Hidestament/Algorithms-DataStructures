#########################################################################################
# AVL木: 以下の操作を全て O(log N) で行う
# insert(key, value): key-value の挿入.
# delete(key): key-value の削除
# x in AVL: key xの存在判定.
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
# ARC033 C - データ構造 (1123ms): https://atcoder.jp/contests/arc033/submissions/30928167
# 参考
# https://stnkien.hatenablog.com/entry/avl-tree
# http://wwwa.pikara.ne.jp/okojisan/avl-tree/index.html
# https://qiita.com/mikecat_mixc/items/e9f8248de2ae7f7a0a29
#########################################################################################

#########################################################################################
# TODO
# 1. 高速化
#   - クラスの属性アクセスは遅い -> Nodeをリストにする
#   - 番兵入れた方が良い?
# 2. cnt(x)の実装
#   - x以下の要素の個数を取得
# 3. 重複を許す場合への対応
#   - 存在する要素があったときもこれまで通りinsertすれば良い
#   - delete がちょっとめんどくさい
#########################################################################################


class Node:
    """AVL木上の各データを表すノード

    Attributes:
        key (any): ノードのキー. 比較可能である必要がある.
        value (any): ノードの値 (保存したいデータ)
        left (Node): 左の子ノード
        right (Node): 右の子ノード
        bias (int): 平衡度 = (左の部分木の高さ) - (右の部分木の高さ)
        size (int): 部分木のサイズ（自分を含む）
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.bias = 0
        self.size = 1

    def __repr__(self):
        return str(self.value)


class AVLTree:
    """AVL木: 非再帰, 重複無し

    Attributes:
        root (Node): 根ノード. default to None
    """

    def __init__(self):
        self.root = None

    def _rotateL(self, u: Node):
        """uに対する左1重回転

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

        # biasの修正
        if v.bias == -1:
            v.bias = u.bias = 0
        else:
            v.bias = 1
            u.bias = -1
        return v

    def _rotateR(self, u: Node):
        """uに対する右1重回転

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

        # biasの修正
        if v.bias == 1:
            v.bias = u.bias = 0
        else:
            v.bias = -1
            u.bias = 1
        return v

    def _update_bias(self, u: Node):
        """2重回転後のbiasの変更

        Args:
            u (Node): 2重回転後の部分木
        """
        if u.bias == 1:
            u.right.bias = -1
            u.left.bias = 0
        elif u.bias == -1:
            u.right.bias = 0
            u.left.bias = 1
        else:
            u.right.bias = 0
            u.left.bias = 0
        u.bias = 0

    def _rotateLR(self, u: Node):
        """uに対する左・右2重回転

        Args:
            u (Node): 対象の部分木

        Returns:
            Node: 左・右回転をした結果の部分木
        """
        v = u.left
        w = v.right

        # sizeの修正
        w.size = u.size
        u.size -= (v.size) - (w.right.size if w.right is not None else 0)
        v.size -= (w.right.size + 1 if w.right is not None else 1)

        # vに対して左回転
        v.right = w.left
        w.left = v

        # uに対して右回転
        u.left = w.right
        w.right = u

        # biasの変更
        self._update_bias(w)
        return w

    def _rotateRL(self, u: Node):
        """uに対する右・左2重回転

        Args:
            u (Node): 対象の部分木

        Returns:
            Node: 右・左回転をした結果の部分木
        """
        v = u.right
        w = v.left

        # sizeの修正
        w.size = u.size
        u.size -= (v.size) - (w.left.size if w.left is not None else 0)
        v.size -= (w.left.size + 1 if w.left is not None else 1)

        # vに対して右回転
        v.left = w.right
        w.right = v

        # nodeに対して左回転
        u.right = w.left
        w.left = u

        # biasの変更
        self._update_bias(w)
        return w

    def _balance(self, path: list, t: int):
        """path上の頂点の回転を行う

        Args:
            path (List[Node, int]): 回転を行うパス上の頂点
            t (int): deleteのとき-1, insertのとき1

        Note:
            - 高さが変わると, その後のnodeで修正が必要になる
            - |bias| = 2 なら, 回転が必要になる
        """
        child = None
        active = True
        while path:
            u, direction = path.pop()
            u.size += t

            # 回転などにより, 子に変更があったら繋ぎ変える
            if child is not None:
                if direction == 1:
                    u.left = child
                else:
                    u.right = child

                # 削除: |bias| = 1 なら その後も平衡
                if (child.bias != 0) and (t == -1):
                    active = False

                # 挿入: 回転後のbiasが0になる
                if (child.bias == 0) and (t == 1):
                    active = False

                child = None

            if active:
                u.bias += t * direction
            else:
                continue

            # 挿入: bias=0 なら以降変更必要なし
            if (u.bias == 0) and (t == 1):
                active = False

            # 削除: |bias|=1 なら以降変更必要なし
            elif (abs(u.bias) == 1) and (t == -1):
                active = False

            # 要右回転: 2重回転後の
            elif u.bias == 2:
                if u.left.bias == -1:
                    child = self._rotateLR(u)
                else:
                    child = self._rotateR(u)

            # 要回転
            elif u.bias == -2:
                if u.right.bias == 1:
                    child = self._rotateRL(u)
                else:
                    child = self._rotateL(u)

        if child is not None:
            self.root = child

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

        # 空のAVLだったら, 根に追加する
        if self.root is None:
            self.root = Node(key, value)
            return

        # 挿入場所までのpathを取得
        path = self._search(key)

        # keyが同じモノが存在すれば, 値の上書き
        now, direction = path[-1]
        if direction == 0:
            now.value = value
            return

        # 挿入
        if direction == 1:
            now.left = Node(key, value)
        else:
            now.right = Node(key, value)

        # 回転
        self._balance(path, 1)

    def delete(self, key):
        """keyの削除

        Args:
            key (any): 削除対象のキー

        Returns:
            any: 削除するkeyのvalue. 削除keyが存在しなければNone
        """
        path = self._search(key)

        # keyが存在しないとき
        if not path:
            return None

        rm_node, direction = path.pop()
        if direction != 0:
            return None

        rm_value = rm_node.value

        # 削除ノードが左部分木を持つ場合, 左部分木の最大値ノードと交換してから削除
        if rm_node.left is not None:
            path.append((rm_node, 1))
            left_max = rm_node.left
            while left_max.right is not None:
                path.append((left_max, -1))
                left_max = left_max.right

            # 左部分木の最大ノードに付いたら, nowと交換
            rm_node.key = left_max.key
            rm_node.value = left_max.value

            rm_node = left_max

        # rm_node: 削除ノード
        # child: 削除ノードの子ノード
        child = rm_node.right if rm_node.left is None else rm_node.left

        # 削除ノードが根の場合
        if not path:
            self.root = child
            return rm_value

        # 削除 & 繋ぎ変え
        par, direction = path[-1]
        if direction == 1:
            par.left = child
        else:
            par.right = child

        # 回転
        self._balance(path, -1)
        return rm_value

    def member(self, key):
        """keyの存在判定

        Args:
            key (any): 存在判定するキー

        Returns:
            bool: keyが存在するかどうか
        """
        path = self._search(key)
        if not path:
            return False

        return key == path[-1][0].key

    def get(self, key):
        """keyのvalueを返す. keyが存在しなければ None を返す

        Args:
            key (nay): 検索対象のkey

        Returns:
            any: 指定したキーに付随するvalue. 存在しなければNone
        """
        path = self._search(key)
        if not path:
            return None

        return path[-1][0].value if path[-1][0].key == key else None

    def lower_bound(self, key):
        """下限探索

        指定したkey以上のモノの中で, 最小のキーを見つける

        Args:
            key (any): キーの下限

        Returns:
            any: 条件を満たすキー. 存在しないならNone.
        """
        lower = float("inf")
        now = self.root
        while now is not None:
            if now.key >= key:
                lower = min(lower, now.key)
                now = now.left
            else:
                now = now.right
        return lower if lower != float("inf") else None

    def upper_bound(self, key):
        """上限探索

        指定したkey"未満"のモノの中で, 最大のキーを見つける

        Args:
            key (any): キーの上限

        Returns:
            any: 条件を満たすキー. 存在しないならNone.
        """
        upper = -float("inf")
        now = self.root
        while now is not None:
            if now.key < key:
                upper = max(upper, now.key)
                now = now.right
            else:
                now = now.left
        return upper if upper != -float("inf") else None

    def kth_element(self, k):
        """小さい方からk番目の要素を見つける

        Args:
            k (int): 何番目か (0-index)

        Note:
            要素がk未満なら, Noneを返す

        Returns:
            any: 条件を満たすkey
        """
        now = self.root
        s = 0
        while now is not None:
            if now.left is not None:
                t = s + now.left.size
            else:
                t = s

            # s + left < k なら 右の子へ, 違うなら左の子へ
            if t == k:
                return now.key
            elif t < k:
                s = t + 1  # now node 分の +1
                now = now.right
            else:
                now = now.left

        return None

    def min_element(self):
        """最小値を返す. 無いならNone
        """
        return self.kth_element(0)

    def max_element(self):
        """最大値を返す. 無いならNone
        """
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

            print(f"parent = {now}")
            print(f"bias = {now.bias}, size = {now.size}")

            left = now.left
            right = now.right
            print(f"left = {left}, right = {right}")
            dfs(left)
            dfs(right)

        dfs(self.root)
        return ""


if __name__ == "__main__":
    import random
    num = [random.randint(0, 10000) for _ in range(30)]
    print(f"min = {min(num)}")
    print(f"max = {max(num)}")

    avl = AVLTree()
    for i in num:
        avl.insert(i)

    print(f"min_avl = {avl.min_element()}")
    print(f"max_avl = {avl.max_element()}")
