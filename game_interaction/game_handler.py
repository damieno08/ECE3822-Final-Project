import os
import sys
import pygame

from .game_session import GameSession
from user_interaction.user import user
from game_interaction.games.Luainid.code.game.main import Game
from game_interaction.games.Luainid.code.game.settings import WIDTH, HEIGTH

start_path = str(sys.path[0])

class Game_Handler:
    
    # basic initialization for making name of game and user
    def __init__(self,user, name):
        self.name = name
        self.user = user
        self._game_session = None

    # empty start_game function to be overwritten by subclass
    def start_game(self):
        self._game_session = GameSession(self.user, self.name)

# Damien's game
class Luaianid(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Luaianid")
        

    # run the game and handle game session recording
    def start_game(self):
        super().start_game()
        self.game = Game(self.user)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score
    

games = [Luaianid(user("Damien"))]