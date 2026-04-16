import socket
import threading
from game_interaction.game import games

class ArcadeServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.games = games # Access to game logic for validation
        self.clients = []

        # Initialize the Socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()
        print(f"[*] Arcade Server listening on {self.host}:{self.port}")
        
        while True:
            conn, addr = self.server.accept()
            # Start a new thread for every client that connects
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.sendall(b"Connected to Arcade Server. Ready for commands.")

        connected = True
        while connected:
            try:
                # Receive message from client
                message = conn.recv(1024).decode()
                
                if not message:
                    break

                print(f"[{addr}] says: {message}")

                # LOGIC: Handle the "CLIENT_RUNNING_GAME_0" signal
                if message == "CLIENT_RUNNING_GAME_0":
                    # The server can now run its own logic for Game 0
                    # For example: verify if the player has permission
                    response = "SERVER: Game 0 verified. Track started."
                    conn.sendall(response.encode())
                    
                    # You can call server-side logic here:
                    # self.games[0].handle_game() 

                else:
                    conn.sendall(b"Command received.")

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break

        print(f"[DISCONNECTED] {addr} closed connection.")
        conn.close()

if __name__ == "__main__":
    # Create and start the server
    arcade_backend = ArcadeServer()
    arcade_backend.start()