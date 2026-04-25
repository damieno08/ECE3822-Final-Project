import os
import sys
import pygame

from .game_session import GameSession
from user_interaction.user import User
from game_interaction.games.game_damien.code.game.settings import WIDTH, HEIGTH

start_path = str(sys.path[0])

class Game_Handler:
    
    # basic initialization for making name of game and user
    def __init__(self,user, name, genre):
        self.name = name
        self.genre = genre
        self.user = user
        self._game_session = None

    # empty start_game function to be overwritten by subclass
    def start_game(self, game_type):
        self._game_session = GameSession(self.user, self.name)
        self.game = game_type(self.user.name)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score

# Damien game
class Damien(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Luaianid", "RPG")
        

    # run the game and handle game session recording
    def start_game(self):
        from game_interaction.games.game_damien.code.game.main import game_damien
        return super().start_game(game_damien)
        
        
    
# Santiago game
class Santiago(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "JAG", "Action")


    # run the game and handle game session recording
    def start_game(self):
        from game_interaction.games.game_santiago.code.game.main import game_santi
        return super().start_game(game_santi)
    
# Paul game
class Paul(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Paul", "Adventure")
        

    # run the game and handle game session recording
    def start_game(self):
        from game_interaction.games.game_paul.code.game.main import game_paul
        return super().start_game(game_paul)
    
# richard's game
class Richard(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Richard", "Puzzle")
        

    # run the game and handle game session recording
    def start_game(self):
        from game_interaction.games.game_richard.code.game.main import game_richard
        return super().start_game(game_richard)
    
