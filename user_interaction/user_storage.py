"""
user_storage.py - User Storage ordered by ASCII-weighted username sum.

Author: Santiago Troya
"""

from datastructures.bst import BST
from datastructures.array import ArrayList
import pickle

# function to get all users from disk
def get_all_users(file):

    # try to get users from file
    try:
        with open(file, "rb") as f:
            users = pickle.load()
    except:
        # make new list if one does not exist
        users = ArrayList()

    return users

# write user data to disk
def set_all_users(file, users):
    
    # open file and dump array
    with open(file, "wb") as f:
        pickle.dump(users, file)

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
