import os
import sys

from .game_session import GameSession
from user_interaction.user import user

start_path = str(sys.path[0])

class Game:
    
    # basic initialization for making name of game and user
    def __init__(self,user, name):
        self.name = name
        self.user = user
        self._game_session = None

    # empty start_game function to be overwritten by subclass
    def handle_game(self):
        self._game_session = GameSession(self.user, self.name)

# Damien's game
class Luaianid(Game):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Luaianid")

    # run the game and handle game session recording
    def handle_game(self):
        super().handle_game()
        start_string = "python3 " + start_path + "/game_interaction/games/Luainid/code/game/main.py " + self.user
        os.system(start_string)
        self._game_session.end_session()
        return self._game_session.get_time_played()
    


games = [Luaianid(user("Damien"))]