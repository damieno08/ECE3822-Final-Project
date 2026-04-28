"""
level.py - Game level with NPC dialog, chat, and networking

Lab 7 — NPC Dialog with Graphs
"""

import pygame
import os

_GAME_DIR = os.path.dirname(os.path.abspath(__file__))

from game_interaction.games.game_santiago.code.game.settings import *
from game_interaction.games.game_santiago.code.game.tile import Tile
from game_interaction.games.game_santiago.code.game.map_loader import load_layer
from game_interaction.games.game_santiago.code.game.character import Character
from game_interaction.games.game_santiago.code.game.subcharacter import get_all_character_classes
from game_interaction.games.game_santiago.code.game.network_client import NetworkClient
from game_interaction.games.game_santiago.code.game.inventory_ui import InventoryUI
from game_interaction.games.game_santiago.code.game.item import create_example_items
from game_interaction.games.game_santiago.code.game.time_travel import TimeTravel
from game_interaction.games.game_santiago.code.game.enemy import Enemy, ENEMY_SPAWN_DATA
from game_interaction.games.game_santiago.code.game.datastructures.patrol_path import PatrolPath
from game_interaction.games.game_santiago.code.game.weapon import Weapon as WeaponSprite
from game_interaction.games.game_santiago.code.game.npc import NPC
from game_interaction.games.game_santiago.code.game.dialog_ui import DialogUI
from game_interaction.chat import Chat
from user_interaction.chat_message import ChatMessage


class Level:
    def __init__(self, player_name, character_class,
                 server_host='localhost', server_port=8080, serializer='text'):
        self.display_surface = pygame.display.get_surface()

        self.floor_sprites      = pygame.sprite.Group()
        self.visible_sprites    = YSortCameraGroup()
        self.obstacle_sprites   = pygame.sprite.Group()
        self.current_attack     = None
        self.attack_sprites     = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.character_class = character_class

        self.create_map()

        self.network   = NetworkClient(player_name, server_host, server_port, serializer)
        self.connected = self.network.connect()

        self.other_players     = {}
        self.font              = pygame.font.Font(None, 24)
        self.connection_status = "Connecting..."

        self.inventory_ui = InventoryUI(self.player.inventory)
        self.inventory_ui.character = self.player
        self.add_starting_items()

        self.time_travel       = TimeTravel(max_history=180)
        self.is_time_traveling = False
        self.enemy_history     = []
        self.enemy_future      = []

        self.enemies = pygame.sprite.Group()
        self.create_enemies()

        self.show_enemy_debug = False

        # NPC / dialog system
        self.npcs      = pygame.sprite.Group()
        self.dialog_ui = None
        self.create_npcs()

        # Chat system
        self.chat              = Chat()
        self.chat_input_active = False
        self.chat_input_text   = ""
        self.chat_log          = []   # ChatMessage objects persisted to user at game end
        self.chat_font         = pygame.font.Font(None, 22)
        self.chat_hint_font    = pygame.font.Font(None, 19)

    # ------------------------------------------------------------------
    # Map, enemies, NPCs
    # ------------------------------------------------------------------

    def create_map(self):
        """Create the game map and player from the three CSV layers."""
        def _map(name):
            return os.path.join(_GAME_DIR, 'map', name)

        floor_blocks = load_layer(_map('map_FloorBlocks.csv'))
        grass        = load_layer(_map('map_Grass.csv'))
        objects      = load_layer(_map('map_Objects.csv'))

        # Background: stretch ground.png over the full WORLD_MAP extent
        map_px_w = len(WORLD_MAP[0]) * TILESIZE
        map_px_h = len(WORLD_MAP)    * TILESIZE

        ground_img_path = os.path.normpath(
            os.path.join(_GAME_DIR, '..', '..', 'graphics', 'tilemap', 'ground.png')
        )
        if os.path.exists(ground_img_path):
            bg_surf = pygame.transform.scale(
                pygame.image.load(ground_img_path).convert_alpha(),
                (map_px_w, map_px_h)
            )
            Tile((0, 0), [self.floor_sprites], 'grass', bg_surf)
        else:
            print(f"[Map] ground.png not found at {ground_img_path}")

        # Object tiles (solid obstacles)
        for (row, col), _ in objects.items():
            Tile((col * TILESIZE, row * TILESIZE), [self.obstacle_sprites], 'boundary')

        # WORLD_MAP: walls + player spawn
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.obstacle_sprites], 'boundary')
                if col == 'p':
                    self.player = self.character_class(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        is_local=True
                    )
                    self.player.create_attack_callback  = self.create_attack
                    self.player.destroy_attack_callback = self.destroy_attack

    def add_starting_items(self):
        for item in create_example_items():
            self.player.inventory.add_item(item)
        for item in self.player.inventory.items:
            if item.item_type == 'weapon':
                self.player.equipped_weapon = item
                break

    def create_enemies(self):
        try:
            for data in ENEMY_SPAWN_DATA:
                combat_kwargs = dict(
                    health=data.get("health", 60),
                    exp=data.get("exp", 30),
                    attack_damage=data.get("attack_damage", 10),
                    notice_radius=data.get("notice_radius", 200),
                    attack_radius=data.get("attack_radius", 60),
                    damage_player=self.damage_player,
                )
                if data["patrol_type"] == "random":
                    enemy = Enemy(
                        name=data["name"],
                        start_x=data["spawn"][0],
                        start_y=data["spawn"][1],
                        patrol_path=None,
                        patrol_type="random",
                        obstacle_sprites=self.obstacle_sprites,
                        speed=data["speed"],
                        sprite_name=data["name"].lower().replace(' ', '_'),
                        **combat_kwargs
                    )
                else:
                    patrol_path = PatrolPath(data["patrol_type"])
                    for waypoint in data["waypoints"]:
                        patrol_path.add_waypoint(waypoint[0], waypoint[1], wait_time=1.0)
                    enemy = Enemy(
                        name=data["name"],
                        start_x=data["spawn"][0],
                        start_y=data["spawn"][1],
                        patrol_path=patrol_path,
                        obstacle_sprites=self.obstacle_sprites,
                        speed=data["speed"],
                        sprite_name=data["name"].lower().replace(' ', '_'),
                        **combat_kwargs
                    )
                self.enemies.add(enemy)
                self.visible_sprites.add(enemy)
                self.obstacle_sprites.add(enemy)
                self.attackable_sprites.add(enemy)
        except Exception as e:
            print(f"Enemy setup error: {e}")

    def create_npcs(self):
        """Spawn NPCs defined in dialog_data.py."""
        try:
            from game_interaction.games.game_santiago.code.game.dialog_data import NPC_DATA
            for entry in NPC_DATA:
                npc = NPC(
                    entry["name"],
                    entry["grid_x"],
                    entry["grid_y"],
                    entry["dialog"],
                    entry["sprite_name"],
                    self.npcs,
                    self.visible_sprites,
                )
                npc.ai_handler = entry.get("ai_handler", None)
            print(f"Spawned {len(self.npcs)} NPC(s).  Press T near an NPC to talk.")
        except Exception as exc:
            import traceback
            print(f"NPC setup error: {exc}")
            traceback.print_exc()

    # ------------------------------------------------------------------
    # Combat
    # ------------------------------------------------------------------

    def create_attack(self):
        self.current_attack = WeaponSprite(self.player,
                                           [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        for attack_sprite in list(self.attack_sprites):
            for enemy in pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False):
                was_alive = enemy.health > 0
                enemy.get_damage(self.player)
                if was_alive and enemy.health <= 0:
                    self.player.exp += enemy.exp

    def damage_player(self, amount):
        self.player.take_damage(amount)

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    def update_network(self):
        if not self.connected:
            self.connection_status = "Disconnected"
            return

        character_type = self.player.character_name.lower()
        status = self.player.status.replace("_idle", "").replace("_attack", "")
        self.network.send_update(self.player.rect.x, self.player.rect.y,
                                  character_type, status)
        updates = self.network.get_updates()

        if updates:
            self.connection_status = (
                f"Connected - {len(updates)} players online "
                f"({self.network.serializer.upper()})"
            )
            current_ids = set()
            for pid, data in updates.items():
                current_ids.add(pid)
                if pid == self.network.my_player_id:
                    continue
                if pid not in self.other_players:
                    ctype = data.get('character_type', '').lower()
                    if not ctype:
                        continue
                    CharClass = None
                    for cls in get_all_character_classes():
                        if cls.get_display_name().lower() == ctype:
                            CharClass = cls
                            break
                    CharClass = CharClass or Character
                    op = CharClass(
                        (data['x'], data['y']),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        player_id=pid, is_local=False
                    )
                    op.name = data['name']
                    self.other_players[pid] = op
                else:
                    op = self.other_players[pid]
                    op.set_position(data['x'], data['y'])
                    op.name = data['name']
                    if 'status' in data:
                        op.status = data['status']

            for pid in set(self.other_players) - current_ids:
                self.other_players[pid].kill()
                del self.other_players[pid]

            self.player.other_players = list(self.other_players.values())

    # ------------------------------------------------------------------
    # NPC dialog
    # ------------------------------------------------------------------

    def _get_nearby_npc(self):
        """Return the first NPC within interaction range, or None."""
        for npc in self.npcs:
            if npc.is_nearby(self.player.rect):
                return npc
        return None

    def handle_dialog_input(self, events):
        """Open dialog on T press if an NPC is nearby; drive active dialog."""
        if self.dialog_ui:
            self.dialog_ui.handle_events(events)
            if self.dialog_ui.is_done():
                self.dialog_ui = None
            return True   # dialog active — suppress movement and chat

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                npc = self._get_nearby_npc()
                if npc:
                    self.dialog_ui = DialogUI(
                        npc.name,
                        npc.dialog_graph,
                        ai_handler=npc.ai_handler
                    )
        return False

    def draw_npc_hints(self):
        """Draw '[T] Talk' above nearby NPCs."""
        offset = (self.visible_sprites.offset.x, self.visible_sprites.offset.y)
        for npc in self.npcs:
            if npc.is_nearby(self.player.rect):
                npc.draw_hint(self.display_surface, offset)

    # ------------------------------------------------------------------
    # Chat system
    # ------------------------------------------------------------------

    def handle_chat_input(self, events):
        """Enter opens chat when no dialog is active and no NPC is nearby."""
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if not self.chat_input_active:
                if event.key == pygame.K_RETURN:
                    self.chat_input_active = True
                    self.chat_input_text = ""
            else:
                if event.key == pygame.K_RETURN:
                    text = self.chat_input_text.strip()
                    if text:
                        msg = ChatMessage(
                            sender=self.network.player_name,
                            text=text,
                            game_id="JAG",
                        )
                        self.chat.send_message(msg)
                        self.chat_log.append(msg)
                        if self.connected:
                            self.network.send_chat(text)
                    self.chat_input_active = False
                    self.chat_input_text = ""
                elif event.key == pygame.K_ESCAPE:
                    self.chat_input_active = False
                    self.chat_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.chat_input_text = self.chat_input_text[:-1]
                else:
                    char = event.unicode
                    if char and char.isprintable() and len(self.chat_input_text) < 80:
                        self.chat_input_text += char

    def update_chat(self):
        """Pull incoming chat messages from the network."""
        if not self.connected:
            return
        for entry in self.network.get_chat_messages():
            msg = ChatMessage(
                sender=entry['sender'],
                text=entry['text'],
                game_id="JAG",
            )
            self.chat.send_message(msg)
            self.chat_log.append(msg)

    def draw_chat_ui(self):
        """Render the last 5 chat messages and, when active, the text input box."""
        PANEL_W  = 420
        MSG_H    = 22
        MAX_SHOW = 5
        PADDING  = 6
        panel_x  = 10
        panel_y  = HEIGHT - 160

        recent = self.chat.recent()[-MAX_SHOW:]

        if recent:
            panel_h    = len(recent) * MSG_H + PADDING * 2
            panel_surf = pygame.Surface((PANEL_W, panel_h), pygame.SRCALPHA)
            panel_surf.fill((0, 0, 0, 140))
            self.display_surface.blit(panel_surf, (panel_x, panel_y - panel_h))
            for i, line in enumerate(recent):
                text_surf = self.chat_font.render(line, True, (230, 230, 230))
                self.display_surface.blit(
                    text_surf,
                    (panel_x + PADDING, panel_y - panel_h + PADDING + i * MSG_H)
                )

        if self.chat_input_active:
            input_y    = panel_y + 4
            input_surf = pygame.Surface((PANEL_W, 28), pygame.SRCALPHA)
            input_surf.fill((0, 0, 0, 180))
            self.display_surface.blit(input_surf, (panel_x, input_y))
            pygame.draw.rect(self.display_surface, (100, 200, 100),
                             (panel_x, input_y, PANEL_W, 28), 1)
            cursor       = "|" if pygame.time.get_ticks() % 800 < 400 else " "
            display_text = f"> {self.chat_input_text}{cursor}"
            self.display_surface.blit(
                self.chat_font.render(display_text, True, (180, 255, 180)),
                (panel_x + PADDING, input_y + 5)
            )
        else:
            hint = self.chat_hint_font.render("Enter: Chat", True, (150, 150, 150))
            self.display_surface.blit(hint, (panel_x, panel_y + 4))

    # ------------------------------------------------------------------
    # HUD / drawing helpers
    # ------------------------------------------------------------------

    def handle_events(self, events):
        if self.chat_input_active:
            return
        for event in events:
            self.inventory_ui.handle_event(event, self.player)

    def draw_names(self):
        if self.network.my_player_id is not None:
            name_text = f"{self.network.player_name} ({self.player.character_name})"
            surf = self.font.render(name_text, True, (0, 255, 0))
            rect = surf.get_rect(center=(self.player.rect.centerx,
                                         self.player.rect.top - 10))
            self.display_surface.blit(
                surf, self.visible_sprites.offset_from_world(rect.topleft))
        for op in self.other_players.values():
            surf = self.font.render(op.name, True, (100, 100, 255))
            rect = surf.get_rect(center=(op.rect.centerx, op.rect.top - 10))
            self.display_surface.blit(
                surf, self.visible_sprites.offset_from_world(rect.topleft))

    def draw_status(self):
        status_color = (0, 255, 0) if self.connected else (255, 100, 100)
        self.display_surface.blit(
            self.font.render(self.connection_status, True, status_color), (10, 10))
        self.display_surface.blit(
            self.font.render(
                "I: Inventory | SPACE: Attack | T: Talk to NPC | Enter: Chat",
                True, (255, 255, 255)), (10, 40))

        bar_rect  = pygame.Rect(10, 70, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        ratio     = max(0.0, self.player.hp / max(1, self.player.max_hp))
        fill_rect = pygame.Rect(10, 70, int(HEALTH_BAR_WIDTH * ratio), BAR_HEIGHT)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,     bar_rect)
        pygame.draw.rect(self.display_surface, HEALTH_COLOR,    fill_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bar_rect, 2)
        self.display_surface.blit(
            self.font.render(f"HP {self.player.hp}/{self.player.max_hp}",
                             True, (255, 255, 255)),
            (10 + HEALTH_BAR_WIDTH + 8, 70))
        self.display_surface.blit(
            self.font.render(f"XP: {self.player.exp}", True, (255, 215, 0)),
            (10, 100))
        if self.player.equipped_weapon:
            w     = self.player.equipped_weapon
            msg   = f"Weapon: {w.name}  (+{w.attack_bonus} atk)"
            color = (255, 200, 100)
        else:
            msg   = "Weapon: none  (I -> select -> Equip)"
            color = (150, 150, 150)
        self.display_surface.blit(
            self.font.render(msg, True, color), (10, 125))

    # ------------------------------------------------------------------
    # Time travel
    # ------------------------------------------------------------------

    def _snapshot_enemies(self):
        enemies = []
        for enemy in self.enemies:
            enemies.append({
                'x': enemy.rect.x, 'y': enemy.rect.y,
                'target_waypoint': enemy.target_waypoint,
                'patrol_active': enemy.patrol_active,
                'is_waiting': enemy.is_waiting,
                'wait_timer': enemy.wait_timer,
                'patrol_current':   enemy.patrol_path.current   if enemy.patrol_path else None,
                'patrol_direction': enemy.patrol_path.direction if enemy.patrol_path else None,
                'wander_target': getattr(enemy, 'wander_target', None),
                'health': enemy.health,
                'combat_status': enemy.combat_status,
            })
        return {'enemies': enemies, 'player_hp': self.player.hp}

    def _restore_enemies(self, snapshot):
        enemy_list = snapshot['enemies'] if isinstance(snapshot, dict) else snapshot
        for enemy, state in zip(self.enemies, enemy_list):
            enemy.rect.x = state['x']; enemy.rect.y = state['y']
            enemy.x = float(enemy.rect.x); enemy.y = float(enemy.rect.y)
            enemy.hitbox.center = enemy.rect.center
            enemy.target_waypoint = state['target_waypoint']
            enemy.patrol_active   = state['patrol_active']
            enemy.is_waiting      = state['is_waiting']
            enemy.wait_timer      = state['wait_timer']
            if enemy.patrol_path:
                enemy.patrol_path.current   = state['patrol_current']
                enemy.patrol_path.direction = state['patrol_direction']
            if hasattr(enemy, 'wander_target'):
                enemy.wander_target = state['wander_target']
            enemy.health        = state.get('health', enemy.health)
            enemy.combat_status = state.get('combat_status', 'patrol')
        if isinstance(snapshot, dict):
            self.player.hp = snapshot.get('player_hp', self.player.hp)
            self.player.vulnerable = True

    def record_player_state(self):
        if not self.is_time_traveling and not self.connected:
            prev = self.time_travel.get_history_size()
            self.time_travel.record_state(self.player.rect.x, self.player.rect.y)
            if self.time_travel.get_history_size() > prev:
                self.enemy_history.append(self._snapshot_enemies())
                while len(self.enemy_history) > self.time_travel.max_history:
                    self.enemy_history.pop(0)
                self.enemy_future.clear()

    def handle_time_travel_input(self, events):
        if self.connected:
            self.is_time_traveling = False
            return
        if self.chat_input_active:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.time_travel.can_rewind():
                    state = self.time_travel.rewind()
                    if state:
                        self.player.rect.x = state.player_x
                        self.player.rect.y = state.player_y
                        self.player.hitbox.center = self.player.rect.center
                        self.is_time_traveling = True
                        if self.enemy_history:
                            self.enemy_future.append(self.enemy_history.pop())
                            if self.enemy_history:
                                self._restore_enemies(self.enemy_history[-1])
                elif event.key == pygame.K_f and self.time_travel.can_replay():
                    state = self.time_travel.replay()
                    if state:
                        self.player.rect.x = state.player_x
                        self.player.rect.y = state.player_y
                        self.player.hitbox.center = self.player.rect.center
                        self.is_time_traveling = True
                        if self.enemy_future:
                            snap = self.enemy_future.pop()
                            self.enemy_history.append(snap)
                            self._restore_enemies(snap)
                else:
                    self.is_time_traveling = False

    def draw_time_travel_ui(self):
        font_small = pygame.font.Font(None, 24)
        if not self.connected:
            if self.is_time_traveling:
                font_large = pygame.font.Font(None, 48)
                text = font_large.render("TIME TRAVELING", True, (255, 100, 100))
                self.display_surface.blit(text, text.get_rect(center=(WIDTH // 2, 50)))
            self.display_surface.blit(
                font_small.render(
                    f"History: {self.time_travel.get_history_size()} | "
                    f"Future: {self.time_travel.get_future_size()}",
                    True, (255, 255, 255)), (10, 155))
            self.display_surface.blit(
                font_small.render("R: Rewind | F: Replay", True, (200, 200, 200)),
                (10, 178))
        else:
            self.display_surface.blit(
                font_small.render("Time travel disabled (multiplayer)",
                                  True, (150, 150, 150)), (10, 155))

    # ------------------------------------------------------------------
    # Enemy debug
    # ------------------------------------------------------------------

    def handle_enemy_debug_input(self, events):
        if self.chat_input_active:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.show_enemy_debug = not self.show_enemy_debug
                elif event.key == pygame.K_m:
                    for enemy in self.enemies:
                        enemy.reset_patrol()

    def draw_enemy_debug(self):
        if not self.show_enemy_debug:
            return
        offset = (self.visible_sprites.offset.x, self.visible_sprites.offset.y)
        y_off = 200
        for enemy in self.enemies:
            surf = pygame.font.Font(None, 20).render(
                enemy.get_debug_status(), True, (255, 255, 100))
            self.display_surface.blit(surf, (10, y_off))
            y_off += 22
            enemy.draw_debug_info(self.display_surface, offset)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self, events):
        # Dialog takes priority — freeze all other input while talking
        dialog_active = self.handle_dialog_input(events)

        if not dialog_active:
            self.handle_events(events)
            self.handle_chat_input(events)
            self.handle_time_travel_input(events)
            self.handle_enemy_debug_input(events)
            self.update_network()
            self.update_chat()

            if not self.chat_input_active:
                self.player.update()
            for op in self.other_players.values():
                op.update()

            if not self.is_time_traveling:
                for enemy in list(self.enemies):
                    enemy.enemy_update(self.player)
                self.enemies.update()
                self.player_attack_logic()

        # Camera offset clamped to map bounds
        map_w = len(WORLD_MAP[0]) * TILESIZE
        map_h = len(WORLD_MAP)    * TILESIZE
        raw_x = self.player.rect.centerx - self.visible_sprites.half_width
        raw_y = self.player.rect.centery - self.visible_sprites.half_height
        cam_offset = pygame.math.Vector2(
            max(0, min(raw_x, map_w - WIDTH)),
            max(0, min(raw_y, map_h - HEIGHT))
        )

        # Floor first, then Y-sorted sprites on top
        for sprite in self.floor_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.topleft - cam_offset)

        self.visible_sprites.custom_draw(self.player, cam_offset)

        if not dialog_active:
            self.record_player_state()

        self.draw_names()
        self.draw_npc_hints()
        self.draw_status()
        self.draw_time_travel_ui()
        self.draw_enemy_debug()
        self.draw_chat_ui()

        if self.inventory_ui.active:
            self.inventory_ui.draw(self.display_surface)

        # Dialog box renders on top of everything
        if self.dialog_ui:
            self.dialog_ui.draw(self.display_surface)


# ---------------------------------------------------------------------------

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width  = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, cam_offset=None):
        if cam_offset is not None:
            self.offset.x = cam_offset.x
            self.offset.y = cam_offset.y
        else:
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            self.display_surface.blit(sprite.image,
                                      sprite.rect.topleft - self.offset)

    def offset_from_world(self, world_pos):
        return pygame.math.Vector2(world_pos) - self.offset
