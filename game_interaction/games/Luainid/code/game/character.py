"""
character.py - Character classes with inventory AND networking support

Integrated version combining:
- lab-03's Character class (inventory, animations, stats)
- project-01's Player class (networking, multiplayer)
"""

import pygame
from games.Luainid.code.game.settings import *
from games.Luainid.code.game.support import import_folder
from games.Luainid.code.game.inventory import Inventory
from games.Luainid.code.game.item import Weapon

class Character(pygame.sprite.Sprite):
    """Base Character class with inventory and networking"""
    
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(groups)
        
        # Basic sprite setup
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-48, -40)
        
        # Character stats
        self.character_name = "Unknown"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 10, 5
        self.exp = 0
        self.equipped_weapon = Weapon("No Weapon", "No Weapon", "", 0)
        
        # Graphics setup
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = None

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        
        # Inventory system
        self.inventory = Inventory(max_size=20)
        
        # Network properties (from project-01)
        self.player_id = player_id
        self.is_local = is_local
        self.name = ""
        self.other_players = []
        
        # For smooth network interpolation (remote players only)
        if not is_local:
            self.target_x = pos[0]
            self.target_y = pos[1]
            self.interpolation_speed = 0.3
        
        # Color tint for other players
        if not is_local:
            self.image = self.image.copy()
            self.image.fill((100, 100, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)

    def import_player_assets(self, animate=True):
        """Load character animations"""
        character_path = '../graphics/characters/' + self.character_name.lower() + "/"
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': []
        }

        for animation in self.animations.keys():
            # Special case: hobbit uses 'west' instead of 'right'
            folder_name = animation
            if animation == 'right' and self.character_name.lower() == 'hobbit':
                folder_name = 'west'
            
            full_path = character_path + folder_name
            if animate:
                try:
                    self.animations[animation] = import_folder(full_path)
                except:
                    # Fallback to single image
                    path = '../graphics/characters/' + self.character_name.lower() + '.png'
                    try:
                        self.animations[animation] = [pygame.image.load(path).convert_alpha()]
                    except:
                        # Ultimate fallback
                        surf = pygame.Surface((64, 64))
                        surf.fill((255, 0, 255))
                        self.animations[animation] = [surf]
            else: 
                path = '../graphics/characters/' + self.character_name.lower() + '.png'
                try:
                    self.animations[animation] = [pygame.image.load(path).convert_alpha()]
                except:
                    surf = pygame.Surface((64, 64))
                    surf.fill((255, 0, 255))
                    self.animations[animation] = [surf]

    def input(self):
        """Handle input - only for local player"""
        if not self.is_local:
            return
            
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Attack input 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

    def get_status(self):
        """Update animation status"""
        # Idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')
    
    def move(self, speed):
        """Move the character"""
        if self.is_local:
            # Local player: physics-based movement
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            
            self.rect.center = self.hitbox.center
        else:
            # Remote players: smooth interpolation
            self.interpolate_to_target()
    
    def set_position(self, x, y):
        """Set position (network update)"""
        if self.is_local:
            self.rect.x = x
            self.rect.y = y
            self.hitbox.center = self.rect.center
        else:
            self.target_x = x
            self.target_y = y
    
    def interpolate_to_target(self):
        """Smoothly move towards target position"""
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        
        self.rect.x += dx * self.interpolation_speed
        self.rect.y += dy * self.interpolation_speed
        self.hitbox.center = self.rect.center
    
    def collision(self, direction):
        """Handle collision with obstacles"""
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Check if sprite has hitbox attribute
                sprite_box = sprite.hitbox if hasattr(sprite, 'hitbox') else sprite.rect
                if sprite_box.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite_box.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite_box.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                sprite_box = sprite.hitbox if hasattr(sprite, 'hitbox') else sprite.rect
                if sprite_box.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite_box.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite_box.bottom
        
        # Player collision (only for local player)
        if self.is_local:
            self.collision_with_players(direction)
    
    def collision_with_players(self, direction):
        """Prevent overlap with other players"""
        if direction == 'horizontal':
            for other_player in self.other_players:
                if other_player.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = other_player.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = other_player.hitbox.right
        
        if direction == 'vertical':
            for other_player in self.other_players:
                if other_player.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = other_player.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = other_player.hitbox.bottom
    
    def cooldowns(self):
        """Handle attack cooldowns"""
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        """Animate the character"""
        if self.animations is None:
            return
            
        # Get current animation
        anim_key = self.status.replace("_idle", "").replace("_attack", "")
        if anim_key not in self.animations:
            anim_key = 'down'
        
        animation = self.animations[anim_key]
        
        # Safety check: if animation list is empty, skip
        if not animation or len(animation) == 0:
            return

        # Loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        # Apply tint for remote players
        if not self.is_local:
            self.image = self.image.copy()
            self.image.fill((100, 100, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        """Update character state"""
        self.input()
        self.cooldowns()
        self.get_status()
        if self.animations:
            self.animate()
        self.move(self.speed)

    def special_ability(self):
        """Special ability - override in subclasses"""
        pass
    
    @staticmethod
    def get_display_name():
        return "Unknown"
    
    @staticmethod
    def get_description():
        return "A mysterious character"
    
    @staticmethod
    def get_preview_image():
        return '../graphics/test/player.png'
    
    def take_damage(self, amount):
        """
        Handles changing character health after attack

        Inputs:
            amount (int): base damage applied

        Outputs:
            actual_damage (int): damage taken after defense

        """

        # Check damage taken based on defense
        #
        actual_damage = self.__apply_defense(amount)
        self.hp -= actual_damage

        if self.hp < 0:
            self.hp = 0

        return actual_damage
    
    # This method is protected because we want no one to change character heath without
    # the proper permissions
    #
    def _heal(self, amount):
        """
        Heal character making sure they do not go beyond maximum hp

        Inputs:
            amount (int): base healing that should be applied to character

        Outputs:
            heal (int): actual healing after applying stats

        """
        
        heal = amount + self.healing
        self.hp +=heal

        # Check to balance at maximum hp
        #
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        return heal
    
    # This method is public because we want anyone to be able to tell our character is
    # alive or dead
    #
    def is_alive(self):
        """Tells if the player is dead or alive"""

        # If hp is not 0 or less return we're alive
        #
        if self.hp > 0:
            return True
        return False
    

    # This is protected because we want our level-up to be called only by the class
    def _level_up(self):
        """
        This function will handle the stat increase from a level-up. Later on
        these xp values and stat increases may change.
        """

        xp_requirement = self.level * 50

        if self.xp >= xp_requirement:
        
            self.level +=1

            # Figure out actual stat increase later
            #
            return self.__change_stats(5,5,5,5,5,5)
        
        raise ValueError("Not enough XP to level up but function was called")


    # Private method to change stats because no-one should change this themself
    #
    def __change_stats(self, max_hp, physical_attack, magical_attack, defense, speed, healing):
        """
        Each value in the declaration of this method is how much the base stat will increase

        Inputs:
            self (int): Character Class
            max_hp (int): increase of hitpoints
            physical_attack (int): increase in physical damage a class gets
            magical_attack (int): An integer describing how much stronger magical attacks get
            defense (int): =increase of damage reduction
            speed (int): increase of character movement
            healing (int): increase of healing power
        
        Output:
            Array of all stats
        """

        # Handle when hp is not at maximum for level-up
        #
        if self.hp < self.max_hp:
            if self.hp > 0:
                hpRatio = self.hp/self.max_hp
            else: 
                hpRatio = 0.05 # 5% health after level up if dead
        else:
            hpRatio = 1
        
        
        self.max_hp += max_hp

        # Change all stats besides hp
        #
        self.hp = self.max_hp*hpRatio
        self.physical_attack += physical_attack
        self.magical_attack += magical_attack
        self.defense += defense
        self.speed += speed
        self.healing += healing

        return [self.level, self.hp, self.max_hp, self.physical_attack, self.magical_attack, self.defense, self.speed, self.healing]


    # Public because anyone should be able to check character stats
    #
    def get_stats(self):
        """
        This function will list all the current stats of a character without changing them.
        """

        return [self.level, self.hp, self.max_hp, self.physical_attack, self.magical_attack, self.defense, self.speed, self.healing]

    # Protected because we want only the class to call this when available    
    def _special_ability(self):
        """Special ability - override in subclasses"""
        pass

    def attack(self, type="physical"):
        """
        This function will handle all damage interaction

        Inputs:
            damage (int): The damage number of our weapon that determines hitpoints lost.
            type (string): The type of damage we would like to deal
            
        Outputs:
            damage_dealt(int): The damage points an enemy will actually take.

        """
        
        damage = 10

        if type == "magical":
            return self._magical_damage(damage) 
        else:
            damage = self.equipped_weapon.attack_bonus
            return self._physical_damage(damage) 


    # Protected as we don't want anyone to have infinite attack calls
    def _physical_damage(self, damage):
        """
        This function will determine how much damage a should produce from physical attacks.
        
        Inputs:
            damage (int): The damage number of our weapon that determines hitpoints lost.

        Outputs:
            actual_damage(int): The damage points an enemy will actually take.
        """

        actual_damage = self.physical_attack + damage
        if actual_damage < 0: actual_damage = 0

        return actual_damage
    
    # Protected as we don't want anyone to have infinite attack calls
    def _magical_damage(self, damage):
        """
        This function will determine how much damage a character should produce 
        from magical attacks.
        
        Inputs:
            damage (int): The damage number of our weapon that determines hitpoints lost.

        Outputs:
            actual_damage(int): The damage points an enemy will actually take.
        """

        actual_damage = self.magical_attack + damage
        if actual_damage < 0: actual_damage = 0

        return actual_damage
    
    def __apply_defense(self,damage):

        """

        Reduce damage taken by accounting for defense. This damage cannot be negative

        Inputs:
            damage (int): base damage
        
        Outputs:
            amount (int): actual damage taken after reduction

        """
        amount = damage - self.defense

        # Make sure damage taken is a positive value
        #
        if amount <= 0:
            amount = 0

        return amount
    
