"""
network_client.py - Network client for multiplayer game

Handles connection to game server with support for three serialization formats:
- TEXT: Pipe-delimited (id|name|x|y|socket)
- JSON: {"id":1,"name":"Alice","x":100,"y":200,"socket":5}
- BINARY: Fixed 88-byte struct

Usage:
    client = NetworkClient("Alice", serializer='text')
    client = NetworkClient("Bob", serializer='json')
    client = NetworkClient("Charlie", serializer='binary')
"""

import socket
import threading
import json
import struct
from queue import Queue

class NetworkClient:
    def __init__(self, game_name, player_name, server_host='localhost', server_port=8080, serializer='text'):
        self.game_name = game_name
        self.player_name = player_name
        self.server_host = server_host
        self.server_port = server_port
        self.serializer = serializer.lower()  # 'text', 'json', or 'binary'
        
        if self.serializer not in ['text', 'json', 'binary']:
            raise ValueError(f"Invalid serializer: {serializer}. Must be 'text', 'json', or 'binary'")
        
        self.sock = None
        self.connected = False
        self.my_player_id = None
        
        self.update_queue = Queue()
        self.receiver_thread = None
        self.running = False
        
        print(f"Network client using {self.serializer.upper()} serialization")
        
    def connect(self):
        """Connect to game server"""
        try:
            print(f"Connecting to {self.server_host}:{self.server_port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))

            # Send JOIN handshake — server is blocking waiting for this
            join_msg = f"JOIN|{self.game_name}|{self.player_name}\n"
            self.sock.sendall(join_msg.encode('utf-8'))

            self.connected = True
            self.running = True
            
            self.receiver_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receiver_thread.start()
            
            print(f"Connected to server using {self.serializer.upper()} serialization!")
            return True
            
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.connected = False
            return False
    
    def _receive_loop(self):
        buffer = ""
        state_buffer = []
        in_state = False

        while self.running and self.connected:
            try:
                data = self.sock.recv(4096).decode('utf-8', errors='ignore')
                if not data:
                    print("Server disconnected")
                    self.connected = False
                    break

                buffer += data

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()

                    if not line:
                        continue

                    # ---- STATE START ----
                    if line == "STATE":
                        in_state = True
                        state_buffer = []
                        continue

                    # ---- STATE END ----
                    if line == "END":
                        in_state = False
                        self._process_state(state_buffer)
                        state_buffer = []
                        continue

                    # ---- COLLECT STATE DATA ----
                    if in_state:
                        state_buffer.append(line)
                    else:
                        self._process_message(line)

            except Exception as e:
                if self.running:
                    print(f"Receive error: {e}")
                    self.connected = False
                break
    def _process_state(self, lines):
        """Process full STATE block safely"""
        print(f"[DEBUG] STATE block received: {len(lines)} players")
        players = {}

        for chunk in lines:
            if not chunk or '|' not in chunk:
                print(f"[SKIP] bad chunk: {chunk}")
                continue

            player = self._deserialize_player(chunk)
            if not player:
                continue

            if player.get("game_name") != self.game_name:
                continue

            players[player['id']] = player

        print(f"[DEBUG] Final players parsed: {len(players)}")
        print(f"[DEBUG GAME CHECK] LOCAL='{self.game_name}' REMOTE='{player.get('game_name')}'")
        self.update_queue.put(players)

    def _process_message(self, msg):
        """Process a message from server"""
        # First check message type (before any separator)
        if msg.startswith("CONNECTED|"):
            parts = msg.split('|')
            self.my_player_id = int(parts[1])
            print(f"Assigned player ID: {self.my_player_id}")
            
    
    def _deserialize_player(self, data):
        """Deserialize player data based on format"""
        try:
            if self.serializer == 'text':
                return self._deserialize_text(data)
            elif self.serializer == 'json':
                return self._deserialize_json(data)
            elif self.serializer == 'binary':
                return self._deserialize_binary(data)
        except Exception as e:
            print(f"[ERROR] Deserialization error ({self.serializer} format): {e}")
            print(f"[ERROR] Data received: '{data[:100]}...'")
            print(f"[ERROR] This usually means server and client are using different serializers!")
            print(f"[ERROR] Server might be using a different format than '{self.serializer}'")
            return None
    
    def _deserialize_json(self, data):
        """Deserialize JSON format: {"id":1,"name":"Alice",...}"""
        player = json.loads(data)
        return {
            "game_name": player['game_name'],
            'id': player['id'],
            'name': player['name'],
            'x': player['x'],
            'y': player['y'],
            'character_type': player.get('character_type', ''),
            'status': player.get('status', 'down')
        }
    
    def _deserialize_text(self, data):
        parts = data.split('|')

        if len(parts) < 7:
            print(f"[BAD TEXT] Not enough fields: {parts}")
            return None

        try:
            return {
                'game_name': parts[0],
                'id': int(parts[1]),
                'name': parts[2],
                'x': float(parts[3]),
                'y': float(parts[4]),
                'character_type': parts[5],
                'status': parts[6]
            }
        except Exception as e:
            print(f"[PARSE ERROR] {e}")
            return None

    def _deserialize_binary(self, data):
        import base64
        try:
            raw_bytes = base64.b64decode(data)
            # Format: 32s (game), i (id), 32s (name), f (x), f (y), i (sock), 16s (char), 8s (stat), 16x (pad)
            # Total = 120 bytes
            struct_fmt = '32s i 32s f f i 16s 8s 16x'
            if len(raw_bytes) < struct.calcsize(struct_fmt):
                return None
            
            unpacked = struct.unpack(struct_fmt, raw_bytes[:120])
            
            return {
                'game_name': unpacked[0].decode('utf-8').rstrip('\x00'),
                'id': unpacked[1],
                'name': unpacked[2].decode('utf-8').rstrip('\x00'),
                'x': unpacked[3],
                'y': unpacked[4],
                'character_type': unpacked[6].decode('utf-8').rstrip('\x00'),
                'status': unpacked[7].decode('utf-8').rstrip('\x00')
            }
        except Exception as e:
            print(f"Binary error: {e}")
            return None
    
    def send_update(self, x, y, character_type="", status="down", game_name="SantiGame"):
        """Send position + player state to server (with game isolation)"""

        if not self.connected or self.my_player_id is None:
            return

        # Ensure safe string conversion
        x = float(x)
        y = float(y)

        # Build message
        msg = (
            f"UPDATE|"
            f"{self.my_player_id}|"
            f"{x}|"
            f"{y}|"
            f"{self.player_name}|"
            f"{character_type}|"
            f"{status}|"
            f"{game_name}\n"
        )

        try:
            self.sock.sendall(msg.encode("utf-8"))
        except Exception as e:
            print(f"[NETWORK ERROR] send_update failed: {e}")
            self.connected = False
    
    def get_updates(self):
        """Get most recent update from queue"""
        updates = []
        while not self.update_queue.empty():
            updates.append(self.update_queue.get())
        
        if updates:
            return updates[-1]
        return None
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        self.connected = False
        if self.sock:
            self.sock.close()