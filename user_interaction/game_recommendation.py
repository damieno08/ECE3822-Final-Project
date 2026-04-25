"""
game_recommendation.py - Game Recommendation system
Tracks genres played per user as a sparse matrix (mostly zeros).

Revision History:
    (ST) 04/19/2026 Create initial class
    (ST) 04/25/2026 Implement playtime tracking and merge-sort recommendations
"""

from datastructures.sparse_matrix import SparseMatrix
from algorithms.merge_sort import MergeSort


# Map each game name to a row index in the sparse matrix
GAMES = {
    "Luaianid": 0,
    "JAG":      1,
    "Paul":     2,
    "Richard":  3,
}

# Map each genre to a column index in the sparse matrix
GENRES = {
    "RPG":       0,
    "Action":    1,
    "Adventure": 2,
    "Puzzle":    3,
}


class GameRecommendation(SparseMatrix):

    def __init__(self, rows=10, cols=10):
        super().__init__(rows=rows, cols=cols, default=0)

    def record_play(self, genre, game_name, time_seconds):
        """
        Add time_seconds of playtime for a game under its genre.
        Called by the caller after start_game() returns, using handler.genre.
        """
        if game_name not in GAMES or genre not in GENRES:
            return

        row = GAMES[game_name]
        col = GENRES[genre]
        current = self.get(row, col)
        self.set(row, col, current + time_seconds)

    def recommend(self):
        """
        Return a list of (game_name, total_seconds) sorted by total playtime
        descending — the game with the most time played is recommended first.
        Games with zero playtime are excluded.
        """
        totals = {}
        for item in self.items():
            (row, _), seconds = item
            game_name = _row_to_game(row)
            if game_name:
                totals[game_name] = totals.get(game_name, 0) + seconds

        entries = list(totals.items())
        return MergeSort(entries, key=lambda x: x[1], reverse=True)


def _row_to_game(row):
    for name, idx in GAMES.items():
        if idx == row:
            return name
    return None
