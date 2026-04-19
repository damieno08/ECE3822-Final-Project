"""
bst.py - Binary Search Tree base class
Author: Santiago Troya
"""


class BST:

    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self._root = None
        self._size = 0

    def insert(self, key, value):
        pass

    def search(self, key):
        pass

    def delete(self, key):
        pass

    def inorder(self):
        pass

    def find_rank(self, key):
        pass

    def kth_smallest(self, k):
        pass

    def kth_largest(self, k):
        pass

    def range_query(self, low, high):
        pass

    def find_min(self):
        pass

    def find_max(self):
        pass

    def __len__(self):
        pass
