"""
This program will define the user class for the arcade project of ECE3822

Revision History:
    (DO) 04/10/2026 Create initial program
    (ALL) 04/13/2026 Revise user class to gave all attributes
    (RL) 04/22/2026  Create some methods
    (RL) 04/23/2026 Create some methods
"""

# import all datastructures

from .chat_history import Chat_history
from .play_history import Play_history
from .game_recommendation import GameRecommendation
from datetime import datetime


# class storing user information
class User:
    def __init__(self, name):

        # set username for user so others can find them
        self.name = name

        # give them an id based on hash function of name
        self.__id = self._generate_id(name)

        # g
        self.sprite_path = "sprite path{name.Lower().replace(' ', '_')}.png"

        # id is bucket index

        # store their individual play history
        self.play_history = Play_history()

        # store chat history
        self.chat_history = Chat_history()

        # store sparse matrix to get recommendations
        self.__game_recommendation = GameRecommendation()

    def _generate_id(self, name):
        """
        Generate user ID using ASCII weighted sum
        """
        total = 0
        for i in name:
            total += ord(i)
        return total

    def update_history(self, history_type, session):

        """
        Function takes in session and type of history, then adds to proper history
        """
        
        # check if chat and send to chat history
        if history_type == "chat":
            self.chat_history.set_history(session)

        # if not a chat history, send to game history
        elif history_type == "game":
            self.play_history.set_history(session)

        # if random history is tried, raise error
        else:
            raise TypeError("Only chat or game histories are available for storage.")

    def get_history(self, history_type, idx=-1):

        """
        Function takes in index and type of history, then returns history at index
        """
        
        # check if chat and get history
        if history_type == "chat":
            self.chat_history.get_history(idx)

        # if not a chat history, get game history
        elif history_type == "game":
            self.play_history.get_history(idx)

        # if random history is tried, raise error
        else:
            raise TypeError("Only chat or game histories are available for indexing.")

    def get_total_games(self):
        """
        Return total games played
        """
        return self.play_history.size()

    def get_total_playtime(self):
        """
        Return total play time in seconds
        """
        return self.play_history.get_total_time()

    def get_id(self):
        return self.__id

    def get_profile(self):
        """
        Return user profile
        """
        return {
            "name": self.name,
            "id": self.id,
            "sprite_path": self.sprite_path,
            "games_played": self.get_total_games(),
            "total_playtime_seconds": self.get_total_playtime()
        }