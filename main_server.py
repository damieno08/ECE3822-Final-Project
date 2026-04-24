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
        # Load existing ArrayList from disk
        data = get_all_users(self.db_file)
        if isinstance(data, ArrayList):
            self.main_array = data
        
        # Populate BST for lookup
        for i in range(len(self.main_array)):
            self.users_bst.insert(self.main_array[i].name)
            
        self.server.listen()
        self.server.settimeout(1.0)
        print(f"[*] Server Online at {self.host}:{self.port}")

        try:
            while True:
                try:
                    conn, addr = self.server.accept()
                except OSError:
                    continue
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
        finally:
            set_all_users(self.db_file, self.main_array)
            self.server.close()

    def handle_client(self, conn, addr):
        print(f"[+] New connection: {addr}")
        while True:
            try:
                data = conn.recv(2048).decode()
                if not data: break

                if data.startswith("LOGIN_REQUEST:"):
                    # Protocol: LOGIN_REQUEST:username:password
                    parts = data.split(":")
                    if len(parts) < 3: continue
                    
                    username = parts[1].strip()
                    password_attempt = parts[2].strip()
                    
                    # 1. Find user in the ArrayList
                    user_found = None
                    for i in range(len(self.main_array)):
                        if self.main_array[i].name == username:
                            user_found = self.main_array[i]
                            break
                    
                    if user_found:
                        # 2. Use the User's internal method to hash the login attempt
                        attempt_hash = user_found._generate_id(password_attempt)
                        
                        # 3. Use the PUBLIC getter you added to get the stored hash
                        # This avoids the '_User__password' attribute error entirely
                        stored_hash = user_found.get_pass_hashed()
                        
                        if attempt_hash == stored_hash:
                            conn.sendall(f"SUCCESS:{username}".encode())
                        else:
                            conn.sendall("ERROR:Incorrect password.".encode())
                    else:
                        # 4. Handle new registration
                        # Check BST to see if name is taken (though not in main_array)
                        if self.users_bst.search(username):
                             conn.sendall("ERROR:Username already exists.".encode())
                        else:
                            new_user = User(username, password_attempt)
                            self.main_array.append(new_user)
                            self.users_bst.insert(new_user.name)
                            set_all_users(self.db_file, self.main_array)
                            conn.sendall(f"SUCCESS:{username}".encode())

                elif data.startswith("QUERY_USER:"):
                    search_val = data.split(":")[1].strip().lower()
                    results = []
                    for i in range(len(self.main_array)):
                        u = self.main_array[i]
                        if search_val in u.name.lower():
                            results.append(f"IDX:{i} | ID:{u.get_id()} | NAME:{u.name}")
                    
                    resp = "USER_RESULTS:" + ("\n".join(results) if results else "No users found")
                    conn.sendall(resp.encode())

            except Exception as e:
                # This will now catch and print errors without crashing the whole thread
                print(f"[!] Thread Error with {addr}: {e}")
                break
        conn.close()

if __name__ == "__main__":
    ArcadeServer().start()