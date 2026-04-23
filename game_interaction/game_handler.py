import os
import sys
import pygame

from .game_session import GameSession
from user_interaction.user import user
from game_interaction.games.game_damien.code.game.settings import WIDTH, HEIGTH

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

# Damien game
class Damien(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Luaianid")
        

    # run the game and handle game session recording
    def start_game(self):
        super().start_game()
        from game_interaction.games.game_damien.code.game.main import game_damien
        self.game = game_damien(self.user.name)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score
    
# Santiago game
class Santiago(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Santiago")
        

    # run the game and handle game session recording
    def start_game(self):
        super().start_game()
        from game_interaction.games.game_santiago.code.game.main import game_santi
        self.game = game_santi(self.user.name)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score
    
# Paul game
class Paul(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Paul")
        

    # run the game and handle game session recording
    def start_game(self):
        super().start_game()
        from game_interaction.games.game_paul.code.game.main import game_paul
        self.game = game_paul(self.user.name)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score
    
# richard's game
class Richard(Game_Handler):

    # intialize game with name and user
    def __init__(self, user):
        super().__init__(user, "Richard")
        

    # run the game and handle game session recording
    def start_game(self):
        super().start_game()
        from game_interaction.games.game_richard.code.game.main import game_richard
        self.game = game_richard(self.user.name)
        self.game.run()
        self.score = self.game.level.player.exp
        self._game_session.end_session()
        return self._game_session.get_time_played(), self.score
    
games = [Damien(user("Damien")), Santiago(user("Santi")), Paul(user("Paul")), Richard(user("Richard"))]