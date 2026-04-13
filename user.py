"""
This program will define the user class for the arcade project of ECE3822

Revision History:
    (DO) 04/10/2026 Create initial program
    (ALL) 04/13/2026 Revise user class to gave all attributes

"""

# import all datastructures

from datastructures.sparse_matrix import SparseMatrix

# class storing user information
class user:
    def __init__(self, name):

        # set username for user so others can find them
        self.name = name

        # give them an id based on hash function of name
        self.__id = None

        # id is bucket index

        # store their individual play history
        self.History = None

        # store sparse matrix to get recommendations
        self.__game_recommendation = SparseMatrix()
