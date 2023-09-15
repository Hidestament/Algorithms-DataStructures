# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/ALDS1_8_A/judge/8281815/PyPy3

import sys

from src.DataStructures.BinarySearchTree.binary_search_tree import BinarySearchTree


input = sys.stdin.readline


tree = BinarySearchTree()
Q = int(input())
for _ in range(Q):
    query = list(map(str, input().split()))
    if query[0] == "insert":
        x = int(query[1])
        tree.insert(x)
    else:
        for node in tree.inorder():
            print(f" {node.key}", end="")
        print()
        for node in tree.preorder():
            print(f" {node.key}", end="")
        print()
