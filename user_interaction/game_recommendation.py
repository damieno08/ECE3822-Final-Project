"""
game_recommendation.py - Game Recommendation system
Tracks genres played per user as a sparse matrix (mostly zeros).

Author: Santiago Troya
"""

from datastructures.sparse_matrix import SparseMatrix


class GameRecommendation(SparseMatrix):

    def __init__(self, rows=10, cols=10):
        super().__init__(rows=rows, cols=cols, default=0)

    def record_play(self, genre):
        pass

    def recommend(self):
        pass
