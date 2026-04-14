import os
import sys

from .game_session import GameSession

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

class Luaianid(Game):

    def __init__(self, user):
        super().__init__(user, "Luaianid")

    def handle_game(self):
        super().handle_game()
        start_string = "python3 /home/damien/ECE3822/projects/ECE3822-Final-Project/game_interaction/games/Luainid/code/game/main.py " + self.user
        os.system(start_string)
        self._game_session.end_session()
        return self._game_session.get_time_played()
    


games = [Luaianid("Damien")]