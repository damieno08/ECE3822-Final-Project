"""
user_indexing.py - Maps user IDs to storage indices via HashTable.

Author: Santiago Troya
"""

from datastructures.hash_table import HashTable


class UserIndexing(HashTable):

    def __init__(self):
        super().__init__()

    # function will map user_id to storage location in user array
    def map_user(self, user_id, storage_index):
        self.set(user_id, storage_index)

    def get_index(self, user_id):
        self.get(user_id)

    def remove_user(self, user_id):
        self.delete(user_id)
