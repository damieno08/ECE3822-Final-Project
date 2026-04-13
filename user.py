"""
This program will define the user class for the arcade project of ECE3822

Revision History:
    (DO) 04/10/2026 Create initial program
    (ALL) 04/13/2026 Revise user class to gave all attributes

"""

# import all datastructures

from datastructures.sparse_matrix import SparseMatrix
from chat_history import Chat_history
from play_history import Play_history

# class storing user information
class user:
    def __init__(self, name):

        # set username for user so others can find them
        self.name = name

        # give them an id based on hash function of name
        self.__id = None

        # id is bucket index

        # store their individual play history
        self.play_history = Play_history()

        # store chat history
        self.chat_history = Chat_history()

        # store sparse matrix to get recommendations
        self.__game_recommendation = SparseMatrix()

    def update_history(self, session, history_type):
        
        """
        Function takes in session and type of history, then adds to proper history
        """
        
        # check if chat and send to chat history
        if history_type == "chat":
            self.chat_history.set_history(session)

        # if not a chat history, send to game history
        elif history_type == "game":
            self.play_history.set_history(session)

