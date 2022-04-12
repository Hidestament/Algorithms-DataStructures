###############################################################################################################
# Segment Tree : 区間に関する処理をO(log N) で行う. 1点更新・区間集約 Segment Tree. 非再起・1-index・非可換
# update(i, x): ai = x する
# query(l, r): a[l] ... a[r] を 求める
###############################################################################################################

###############################################################################################################
# Verify
###############################################################################################################

###############################################################################################################
# TODO
# 1. need refactoring
# 2. add docstring
###############################################################################################################


class SegmentTree:
    """ 1点更新・区間集約 Segment Tree. 非再起・1-index・非可換

    Attributes:
        tree (List[Union[int, float]]): セグメントツリーを表す配列
        segfunc (Callable): 集約を行う関数 (モノイド上の演算)
        ide_ele (float): 集約の関数における単位元　（モノイド上の単位元）
        update (int, float): 元の配列の更新 & セグメントツリーの更新
        query (int, int): 区間集約値の取得
    """

    def __init__(self, n: int, ide_ele: float, seg_func: callable):
        """
        Args:
            n (int): 元の配列のサイズ
            ide_ele (float): モノイドにおける単位元
            segfunc (callable): 集約を行う関数 （モノイド上の演算）
        """
        self.segfunc = seg_func
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [self.ide_ele] * (2 * self.num)

    def update(self, i: int, x: float) -> None:
        """元の配列のi番目を x に変更（上書き）する. それに伴ってセグメントツリーも更新する. +=のようなupdateではない.

        Args:
            i (int): 元の配列のi番目の要素. 元の配列の0-indexの
            x (float): 変更後の値
        """
        i += self.num
        self.tree[i] = x
        while i > 1:
            i >>= 1
            self.tree[i] = self.segfunc(
                self.tree[i << 1], self.tree[(i << 1) + 1])

    def query(self, l: int, r: int):
        """元の配列の閉区間[l, r]のsegfuncにおける集約値を取得する

        Args:
            l (int): 元の配列の集約を行う区間の左端のindex. 0-index
            r (int): 元の配列の集約を行う区間の右端のindex. 0-index
        """
        # [l, r) として葉から計算していく
        l += self.num
        r += self.num + 1

        l_res = self.ide_ele
        r_res = self.ide_ele

        while l < r:
            if l & 1:  # lが奇数だったらそのノードを集約する
                l_res = self.segfunc(l_res, self.tree[l])
                l += 1  # 右に進む
            if r & 1:  # rが奇数だったら, rは開区間なので その1つ左ノードを集約する
                r_res = self.segfunc(self.tree[r - 1], r_res)

            l >>= 1  # 上に進む（２で割って切り捨て）
            r >>= 1

        return self.segfunc(l_res, r_res)
