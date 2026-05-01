"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

import os
import pygame
from game_interaction.games.game_santiago.code.game.character import Character

_CHARS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../graphics/characters'))


class Character1(Character):
    """Clown - Tanky and unpredictable"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Clown"
        self.hp, self.max_hp = 130, 130
        self.attack, self.defense = 6, 9

        try:
            self.image = pygame.image.load(os.path.join(_CHARS_DIR, 'clown', 'down', 'frame_000.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        self.import_player_assets(animate=True)

    @staticmethod
    def get_display_name():
        return "Clown"

    @staticmethod
    def get_description():
        return "Tank with high defense"

    @staticmethod
    def get_preview_image():
        return os.path.join(_CHARS_DIR, 'clown', 'down', 'frame_000.png')


class Character2(Character):
    """Jester - Balanced trickster"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Jester"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 11, 6

        try:
            self.image = pygame.image.load(os.path.join(_CHARS_DIR, 'jester', 'down', 'frame_000.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        self.import_player_assets(animate=True)

    @staticmethod
    def get_display_name():
        return "Jester"

    @staticmethod
    def get_description():
        return "Balanced trickster"

    @staticmethod
    def get_preview_image():
        return os.path.join(_CHARS_DIR, 'jester', 'down', 'frame_000.png')


class Character3(Character):
    """Joker - High-risk high-reward"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Joker"
        self.hp, self.max_hp = 75, 75
        self.attack, self.defense = 18, 2

        try:
            self.image = pygame.image.load(os.path.join(_CHARS_DIR, 'joker', 'down', 'frame_000.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        self.import_player_assets(animate=True)

    @staticmethod
    def get_display_name():
        return "Joker"

    @staticmethod
    def get_description():
        return "Glass cannon — highest attack"

    @staticmethod
    def get_preview_image():
        return os.path.join(_CHARS_DIR, 'joker', 'down', 'frame_000.png')


class Character4(Character):
    """Mime - Silent and swift"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Mime"
        self.hp, self.max_hp = 85, 85
        self.attack, self.defense = 13, 5
        self.speed = 7

        try:
            self.image = pygame.image.load(os.path.join(_CHARS_DIR, 'mime', 'down', 'frame_000.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        self.import_player_assets(animate=True)

    @staticmethod
    def get_display_name():
        return "Mime"

    @staticmethod
    def get_description():
        return "Fast and silent"

    @staticmethod
    def get_preview_image():
        return os.path.join(_CHARS_DIR, 'mime', 'down', 'frame_000.png')


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character' and cls.__name__.startswith('Character'):
            character_classes.append(cls)
    return character_classes
