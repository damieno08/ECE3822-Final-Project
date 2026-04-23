import socket
import threading
from user_interaction.user_storage import get_all_users, set_all_users, UserStorage
from user_interaction.user import User 
from datastructures.array import ArrayList 

class ArcadeServer:
    def __init__(self, host='0.0.0.0', port=65432, db_file="users.dat"):
        self.host = host
        self.port = port
        self.db_file = db_file
        self.users_bst = UserStorage()
        self.main_array = ArrayList()
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def start(self):
        data = get_all_users(self.db_file)
        if isinstance(data, ArrayList):
            self.main_array = data
        
        for i in range(len(self.main_array)):
            self.users_bst.insert(self.main_array[i].name)
            
        self.server.listen()
        print(f"[*] Server Online at {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = self.server.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
        finally:
            set_all_users(self.db_file, self.main_array)
            self.server.close()

    def handle_client(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data: break

                if data.startswith("LOGIN_REQUEST:"):
                    parts = data.split(":")
                    username = parts[1].strip()
                    
                    existing_name = self.users_bst.search(username)
                    if not existing_name:
                        new_user = User(username)
                        self.main_array.append(new_user)
                        self.users_bst.insert(new_user.name)
                        # Client looks for "SUCCESS" to trigger dashboard
                        conn.sendall(f"SUCCESS: {new_user.name}".encode())
                    else:
                        conn.sendall(f"SUCCESS: {existing_name}".encode())

                elif data.startswith("QUERY_USER:"):
                    search_val = data.split(":")[1].strip().lower()
                    results = []
                    for i in range(len(self.main_array)):
                        u = self.main_array[i]
                        if search_val in u.name.lower():
                            results.append(f"IDX:{i} | ID:{u.get_id()} | NAME:{u.name}")
                    
                    resp = "USER_RESULTS:" + ("\n".join(results) if results else "No users found")
                    conn.sendall(resp.encode())

            except: break
        conn.close()

if __name__ == "__main__":
    ArcadeServer().start()