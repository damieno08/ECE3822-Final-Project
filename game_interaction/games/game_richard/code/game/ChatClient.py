import socket
import threading

class ChatClient:
    def __init__(self, player_name, host='localhost', port=50080):
        self.player_name = player_name
        self.host = host
        self.port = port

        self.sock = None
        self.running = False
        self.buffer = ""
        self.messages = []

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        # join chat
        self.sock.sendall(f"CHAT_JOIN|{self.player_name}\n".encode())

        self.running = True
        threading.Thread(target=self._recv_loop, daemon=True).start()

    def _recv_loop(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break

                self.buffer += data

                while '\n' in self.buffer:
                    line, self.buffer = self.buffer.split('\n', 1)

                    if line.startswith("CHAT_BROADCAST"):
                        _, sender, text = line.split("|", 2)
                        self.messages.append((sender, text))

            except:
                break

    def send(self, text):
        try:
            self.sock.sendall(
                f"CHAT_MSG|{self.player_name}|{text}\n".encode()
            )
        except:
            pass

    def get_messages(self):
        msgs = self.messages[:]
        self.messages.clear()
        return msgs

    def disconnect(self):
        self.running = False
        if self.sock:
            self.sock.close()