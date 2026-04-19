"""
user_storage.py - User Storage ordered by ASCII-weighted username sum.

Author: Santiago Troya
"""

from datastructures.bst import BST


class UserStorage(BST):

    def __init__(self):
        super().__init__()

    def _ascii_key(self, username):
        pass

    def add_user(self, user):
        pass

    def find_user(self, username):
        pass

    def autocomplete(self, prefix):
        pass
