# https://onlinejudge.u-aizu.ac.jp/status/users/hidexchan/submissions/1/ALDS1_8_B/judge/8281826/PyPy3

import sys

from DataStructures.BinarySearchTree.SearchTree.binary_search_tree import BinarySearchTree


input = sys.stdin.readline


tree = BinarySearchTree()
Q = int(input())
for _ in range(Q):
    query = list(map(str, input().split()))
    if query[0] == "insert":
        x = int(query[1])
        tree.insert(x)
    elif query[0] == "find":
        x = int(query[1])
        print("yes" if x in tree else "no")
    else:
        for node in tree.inorder():
            print(f" {node.key}", end="")
        print()
        for node in tree.preorder():
            print(f" {node.key}", end="")
        print()
