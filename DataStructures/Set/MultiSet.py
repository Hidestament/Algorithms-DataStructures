###############################################################################################################
# MultiSet : 多重集合. Min-MaxがO(log N)
# add(x): 集合にxを1つ加える O(1)
# remove(x, num): 集合内のxをcnt個削除する O(1)
# min: 多重集合内の最小値を求める O(log N)
# max: 多重集合内の最大値を求める O(log N)
# is_exist(x): xの存在判定
###############################################################################################################

###############################################################################################################
# Verify
# ABC253 C - Max - Min Query (727ms): https://atcoder.jp/contests/abc253/submissions/32073992
# 参考
# https://tsubo.hatenablog.jp/entry/2020/06/15/124657
###############################################################################################################

###############################################################################################################
# TODO
# 1. need refactoring
# 2. add docstring
###############################################################################################################


from heapq import heappush, heappop
from collections import defaultdict


class MultiSet:
    def __init__(self):
        self.min_h = []
        self.max_h = []
        self.cnt = defaultdict(int)

    def add(self, x):
        heappush(self.min_h, x)
        heappush(self.max_h, -x)
        self.cnt[x] += 1

    def remove(self, x, num):
        if self.cnt[x] == 0:
            return

        self.cnt[x] = max(0, self.cnt[x] - num)
        while self.min_h:
            if self.cnt[self.min_h[0]] == 0:
                heappop(self.min_h)
            else:
                break

        while self.max_h:
            if self.cnt[-1 * self.max_h[0]] == 0:
                heappop(self.max_h)
            else:
                break

    def is_exist(self, x):
        return self.cnt[x] > 0

    @property
    def min(self):
        return self.min_h[0]

    @property
    def max(self):
        return -1 * self.max_h[0]


if __name__ == "__main__":
    Q = int(input())
    multiset = MultiSet()
    for _ in range(Q):
        q = list(map(int, input().split()))
        if q[0] == 1:
            x = q[1]
            multiset.add(x)
        elif q[0] == 2:
            x, c = q[1], q[2]
            multiset.remove(x, c)
        else:
            print(multiset.max - multiset.min)
