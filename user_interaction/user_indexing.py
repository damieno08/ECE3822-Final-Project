"""
user_indexing.py - Maps user IDs to storage indices via HashTable.

Author: Santiago Troya
"""

from datastructures.hash_table import HashTable


class UserIndexing(HashTable):

    def __init__(self):
        super().__init__()

    def map_user(self, user_id, storage_index):
        pass

    def get_index(self, user_id):
        pass

    def remove_user(self, user_id):
        pass
