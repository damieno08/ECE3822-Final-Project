"""
leaderboard.py - Leaderboard ordered by score (BST).

Revision History:
    (ST) 04/19/2026 Create initial class
"""

from datastructures.bst import BST


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
        """Insert or update a user's score."""
        if user in self._user_scores:
            self.delete((self._user_scores[user], user))
        self._user_scores[user] = score
        self.insert((score, user))

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
        rank_from_bottom = self.find_rank((score, user))
        return len(self) - rank_from_bottom + 1
