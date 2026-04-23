"""
user_storage.py - User Storage ordered by ASCII-weighted username sum.

Revision History:
    (ST) 04/20/2026 Create initial program
    (RL) 04/23/2026 Create some methods
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
