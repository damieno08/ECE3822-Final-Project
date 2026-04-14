
from game import Game
import os

class Luaianid(Game):

    def __init__(self, user, name="Luaianid",):
        super().__init__(name, user)

    def start_game(self):
        start_string = "python3 games/Luainid/code/game/main.py " + self.user
        os.system(start_string)

G = Luaianid("Damien")

G.start_game()