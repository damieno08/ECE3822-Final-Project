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
        """Background thread to receive messages from server"""
        buffer = ""
        
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
                    self._process_message(line)
                    
            except Exception as e:
                if self.running:
                    print(f"Receive error: {e}")
                    self.connected = False
                break
    
    def _process_message(self, msg):
        """Process a message from server"""
        # First check message type (before any separator)
        if msg.startswith("CONNECTED|"):
            parts = msg.split('|')
            self.my_player_id = int(parts[1])
            print(f"Assigned player ID: {self.my_player_id}")
            
        elif msg.startswith("STATE||"):
            # Game state update
            # Format: STATE||<serialized_player1>||<serialized_player2>||...
            # Players are separated by || (double pipe) to avoid conflicts with serialization formats
            parts = msg.split('||')
            print(f"[DEBUG] Received STATE message with {len(parts)-1} player entries")
            players = {}
            
            for i in range(1, len(parts)):
                if parts[i]:
                    print(f"[DEBUG] Parsing player {i}: '{parts[i][:50]}...'")  # First 50 chars
                    player_data = self._deserialize_player(parts[i])
                    if player_data:
                        print(f"[DEBUG] Parsed player: ID={player_data['id']}, Name={player_data['name']}")
                        players[player_data['id']] = player_data
                    else:
                        print(f"[DEBUG] Failed to parse player data")
            
            print(f"[DEBUG] Total players parsed: {len(players)}")
            self.update_queue.put(players)
    
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
        # Expecting at least 6 parts: Game|ID|Name|X|Y|Socket
        if len(parts) >= 6:
            try:
                return {
                    'game_name': parts[0],
                    'id': int(parts[1]),
                    'name': parts[2],
                    'x': float(parts[3]),
                    'y': float(parts[4]),
                    # Index 5 is socket, index 6 is char_type, index 7 is status
                    'character_type': parts[6] if len(parts) > 6 else '',
                    'status': parts[7] if len(parts) > 7 else 'down'
                }
            except (ValueError, IndexError):
                return None
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
    
    def send_update(self, x, y, character_type="", status="down"):
        """Send our position, character type, and status to server (uses standard UPDATE format)"""
        if self.connected and self.my_player_id is not None:
            msg = f"UPDATE|{self.my_player_id}|{x}|{y}|{self.player_name}|{character_type}|{status}\n"
            try:
                self.sock.send(msg.encode('utf-8'))
            except:
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