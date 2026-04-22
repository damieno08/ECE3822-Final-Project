import pygame 
from game_interaction.games.game_paul.code.game.settings import *
import sys

start_path = str(sys.path[0])
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load(start_path + '/game_interaction/games/game_paul/graphics/test/rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		