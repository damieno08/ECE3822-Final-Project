import pygame
from game_interaction.games.Luainid.code.game.settings import *
import os
import sys

start_path = str(sys.path[0])

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None, area_id=0):
        super().__init__(groups)
        self.sprite_type = sprite_type
        
        if surface:
            self.image = surface
        elif sprite_type in ['boundary', 'invisible']:
            self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        else:
            # Hardcoded path mapping based on area_id
            paths = {
                0: {'grass': 'game_interaction/games/Luainid/graphics/tilemap/ground.png', 'object': start_path + 'game_interaction/games/Luainid/graphics/tilemap/wall.png'},
                1: {'grass': start_path + 'game_interaction/games/Luainid/graphics/tilemap/dirt.png',   'object': start_path+ 'game_interaction/games/Luainid/graphics/tilemap/forest_wall.png'},
                2: {'grass': start_path + 'game_interaction/games/Luainid/graphics/tilemap/forge_oven.png', 'object': start_path + 'game_interaction/games/Luainid/graphics/tilemap/forge_wall.png'}
            }
            
            # Get the specific path, defaulting to Area 0 if ID is unknown
            area_paths = paths.get(area_id, paths[0])
            path = area_paths.get(sprite_type)

            if path and os.path.exists(path):
                self.image = pygame.image.load(path).convert_alpha()
            else:
                # Fallback colors if images are missing
                self.image = pygame.Surface((TILESIZE, TILESIZE if sprite_type == 'grass' else TILESIZE * 2))
                self.image.fill('#348C31' if sprite_type == 'grass' else '#5C4033')

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, -10)