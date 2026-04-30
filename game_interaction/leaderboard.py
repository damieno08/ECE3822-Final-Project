"""
leaderboard.py - Leaderboard ordered by score (BST).

Revision History:
    (ST) 04/19/2026 Create initial class
         04/30/2026 Update to support bst_rank.py
Author: Paul Garrison
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datastructures.bst_rank import BST


class Leaderboard(BST):
    """
    Stores (score, user) tuples in the AVL BST so scores are ordered
    naturally.  A separate dict gives O(1) user->score lookups needed
    for rank_of and de-duplication in add_score.
    """

    def __init__(self):
        super().__init__()
        self._user_scores = {}  # {username: score}

    def add_score(self, user, score):
        """
        Insert or update a user's score ONLY if it is higher than their previous best.

        Returns:
            True if leaderboard was updated
            False if score was ignored
        """

        # If user already has a score
        if user in self._user_scores:
            old_score = self._user_scores[user]

            # stop if new score is worse or equal
            if score <= old_score:
                return False

            # remove old score from BST
            self.delete((old_score, user))

        # insert new best score
        self._user_scores[user] = score
        self.insert((score, user))

        return True

    def top_n(self, n):
        """Return [(user, score), ...] for the top n players, highest first."""
        result = []
        for k in range(1, min(n, len(self)) + 1):
            entry = self.kth_largest(k)
            if entry:
                result.append((entry[1], entry[0]))
        return result

    def rank_of(self, user):
        """Return 1-based rank of user (1 = highest score), or None if not found."""
        if user not in self._user_scores:
            return None
        
        score = self._user_scores[user]
        return self.find_rank((score, user)) + 1
    
    def score_of(self, user):
        # return users best score or none
        return self._user_scores.get(user)
    
    def players_with_score(self, score):
        # return sorted list of users with this score
        users = self.search(score)
        return sorted(users) if users else []
