"""
leaderboard.py - Leaderboard ordered by score (BST).

Author: Santiago Troya
"""

from datastructures.bst import BST


class Leaderboard(BST):

    def __init__(self):
        super().__init__()

    def add_score(self, user, score):
        pass

    def top_n(self, n):
        pass

    def rank_of(self, user):
        pass
