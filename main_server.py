import socket
import threading
import pickle
import json
import os
from datetime import datetime, timedelta

from user_interaction.user_storage import get_all_users, set_all_users, UserStorage
from user_interaction.user import User
from user_interaction.chat_message import ChatMessage
from datastructures.array import ArrayList 
from game_interaction.game_session import GameSession
from game_interaction.leaderboard import Leaderboard


class ArcadeServer:
    def __init__(self, host='0.0.0.0', port=65432, db_file="users.dat", lb_file="leaderboards.pkl"):
        self.host = host
        self.port = port
        self.db_file = db_file
        self.lb_file = lb_file

        self.users_bst = UserStorage()
        self.main_array = ArrayList()

        self.game_map = {
            "0": "LUAIANID",
            "1": "JAG",
            "2": "VERMIS",
            "3": "RICHARD",
            "4": "TOM"
        }

        # ✅ Load or create leaderboards
        self.leaderboards = self.load_leaderboards()
        self.chat_clients = []
        self.chat_lock = threading.Lock()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    # --------------------------------------------------
    # LEADERBOARD PERSISTENCE
    # --------------------------------------------------

    def load_leaderboards(self):
        """Load leaderboards from pickle file or create new ones."""
        if os.path.exists(self.lb_file):
            try:
                with open(self.lb_file, "rb") as f:
                    data = pickle.load(f)

                # Ensure all games exist
                for gid in self.game_map:
                    if gid not in data:
                        data[gid] = Leaderboard()

                print("[*] Leaderboards loaded from file")
                return data

            except Exception as e:
                print(f"[!] Failed to load leaderboard file: {e}")

        # If file doesn't exist or fails → create new
        print("[*] Creating new leaderboards")
        return {gid: Leaderboard() for gid in self.game_map}

    def save_leaderboards(self):
        """Save leaderboards to pickle file."""
        try:
            with open(self.lb_file, "wb") as f:
                pickle.dump(self.leaderboards, f)
        except Exception as e:
            print(f"[!] Failed to save leaderboards: {e}")

    # --------------------------------------------------

    def start(self):
        data = get_all_users(self.db_file)
        if isinstance(data, ArrayList):
            self.main_array = data

        for i in range(len(self.main_array)):
            self.users_bst.insert(self.main_array[i].name)

        self.server.listen()
        self.server.settimeout(1.0)  # allow Ctrl+C to interrupt blocking accept() on Windows
        print(f"[*] Server Online at {self.host}:{self.port}")

        try:
            while True:
                try:
                    conn, addr = self.server.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
        finally:
            set_all_users(self.db_file, self.main_array)
            self.save_leaderboards()  # ✅ Save on shutdown
            self.server.close()

    def find_user_by_name(self, name):
        for i in range(len(self.main_array)):
            if self.main_array[i].name == name:
                return self.main_array[i]
        return None

    def handle_client(self, conn, addr):
        print(f"[+] New connection: {addr}")

        while True:
            try:
                raw_data = conn.recv(10240).decode()
                if not raw_data:
                    break

                # ---------------- LOGIN ----------------
                if raw_data.startswith("LOGIN_REQUEST"):
                    parts = raw_data.split("|")
                    if len(parts) < 3:
                        continue

                    u, p = parts[1].strip(), parts[2].strip()
                    user_found = self.find_user_by_name(u)

                    if user_found:
                        if user_found._generate_id(p) == user_found.get_pass_hashed():
                            conn.sendall(f"SUCCESS:{u}".encode())
                        else:
                            conn.sendall("ERROR:Incorrect password.".encode())
                    else:
                        new_user = User(u, p)
                        self.main_array.append(new_user)
                        self.users_bst.insert(u)
                        conn.sendall(f"SUCCESS:{u}".encode())

                # ---------------- SAVE SESSION ----------------
                elif raw_data.startswith("SAVE_SESSION"):
                    parts = raw_data.split("|")
                    if len(parts) < 5:
                        continue

                    uname = parts[1].strip()
                    score_val = float(parts[2])
                    dur_val = parts[3]
                    g_idx = parts[4].strip()

                    gname = self.game_map.get(g_idx, "Unknown Module")
                    user_obj = self.find_user_by_name(uname)

                    if user_obj:
                        # Save session
                        sess = GameSession(user_obj, gname)
                        sess.score = int(score_val)

                        try:
                            h, m, s = map(float, dur_val.split(':'))
                            sess.end_time = sess.start_time + timedelta(hours=h, minutes=m, seconds=s)
                        except:
                            sess.end_time = datetime.now()

                        user_obj.update_history("game", sess)

                        # ✅ Update leaderboard
                        if g_idx in self.leaderboards:
                            self.leaderboards[g_idx].add_score(uname, score_val)
                            self.save_leaderboards()  # ✅ SAVE IMMEDIATELY

                        print(f"[DEBUG] Session Logged: {uname} | {gname} | Score: {score_val}")

                # ---------------- SAVE CHAT BATCH ----------------
                elif raw_data.startswith("SAVE_CHAT"):
                    messages = raw_data.split("\n")

                    for raw in messages:
                        if not raw.startswith("SAVE_CHAT"):
                            continue

                        parts = raw.split("|")

                        if len(parts) < 6:
                            continue

                        user_name = parts[1].strip()
                        game_id   = parts[2].strip()
                        sender    = parts[3].strip()
                        text      = parts[4].strip()
                        timestamp = parts[5].strip()

                        user_obj = self.find_user_by_name(user_name)

                        if user_obj:
                            msg = ChatMessage(
                                sender=sender,
                                text=text,
                                game_id=game_id,
                                timestamp=timestamp,
                                rate_limited=False,
                            )

                            user_obj.update_history("chat", msg)

                            print(f"[DEBUG] Chat saved: {user_name} | {text}")

                # ---------------- GET LEADERBOARD ----------------
                elif raw_data.startswith("GET_LEADERBOARD"):
                    messages = raw_data.split("\n")

                    # default values (IMPORTANT: prevents "unbound local variable" bugs)
                    g_idx = None
                    request_user = None

                    for raw in messages:
                        if not raw.startswith("GET_LEADERBOARD"):
                            continue

                        parts = raw.split("|")

                        # parse game index
                        g_idx = parts[0].split(":")[1].strip()

                        # parse requesting user (optional)
                        if len(parts) > 1:
                            request_user = parts[1].strip()

                    if not g_idx:
                        pass # safety guard
                    else:
                        if g_idx in self.leaderboards:
                            lb = self.leaderboards[g_idx]
                            top = lb.top_n(50)

                            output = f"--- TOP PLAYERS ({self.game_map[g_idx]}) ---\n\n"
                            user_rank = None

                            for i, (user, score) in enumerate(top, start=1):
                                output += f"{user} - {score}\n"
                                if request_user and user == request_user:
                                    user_rank = i

                            # We use a distinct separator (|||) so the client doesn't 
                            # get confused by the newlines inside 'output'
                            rank_msg = f"RANK:{user_rank if user_rank else 'N/A'}"
                            lb_msg = f"LEADERBOARD_DATA:{output}"
                            final_send = f"{rank_msg}|||{lb_msg}\n"

                            print(f"Sending: {rank_msg}") # debug
                            conn.sendall(final_send.encode())
                # ---------------- QUERY USER ----------------
                elif raw_data.startswith("QUERY_USER:"):
                    search_val = raw_data.split(":")[1].strip().lower()
                    results = [
                        f"IDX:{i} | ID:{self.main_array[i].get_id()} | NAME:{self.main_array[i].name}"
                        for i in range(len(self.main_array))
                        if search_val in self.main_array[i].name.lower()
                    ]
                    resp = "USER_RESULTS:" + ("\n".join(results) if results else "No users found")
                    conn.sendall(resp.encode())

                # ---------------- GET_HISTORY (SERVER) ----------------
                elif raw_data.startswith("GET_HISTORY:"):
                    target_name = raw_data.split(":")[1].strip()
                    user_obj = self.find_user_by_name(target_name)

                    if user_obj:
                        # Calculate ranks for all games using the existing sorted leaderboards
                        user_ranks = {}
                        for g_idx in self.game_map.keys():
                            rank = "N/A"
                            if g_idx in self.leaderboards:
                                # top_n is already sorted, so the index + 1 is the rank
                                sorted_lb = self.leaderboards[g_idx].top_n(1000) 
                                for i, (name, score) in enumerate(sorted_lb, start=1):
                                    if name == target_name:
                                        rank = str(i)
                                        break
                            user_ranks[g_idx] = rank

                        # Bundle everything into one payload
                        payload = {
                            "user_obj": user_obj,
                            "ranks": user_ranks
                        }
                        
                        user_bytes = pickle.dumps(payload)
                        header = "USER_PICKLE:".encode()
                        conn.sendall(header + user_bytes)
                    else:
                        conn.sendall("ERROR:User not found".encode())
                # ---------------- LIVE CHAT JOIN----------------
                elif raw_data.startswith("CHAT_JOIN"):
                    username = raw_data.split("|")[1]

                    with self.chat_lock:
                        self.chat_clients.append((conn, username))

                    print(f"[CHAT] {username} joined chat")
                                
                # ---------------- LIVE CHAT HANDLING----------------
                elif raw_data.startswith("CHAT_MSG"):
                    parts = raw_data.split("|", 2)
                    if len(parts) < 3:
                        continue

                    sender = parts[1]
                    text = parts[2]

                    message = f"CHAT_BROADCAST|{sender}|{text}"

                    with self.chat_lock:
                        for client, _ in self.chat_clients:
                            try:
                                client.sendall((message + "\n").encode())
                            except:
                                pass
                # ---------------- RECENTLY PLAYED ----------------
                elif raw_data.startswith("GET_RECENTLY_PLAYED:"):
                    uname = raw_data.split(":")[1].strip()
                    user_obj = self.find_user_by_name(uname)

                    if user_obj:
                        total = user_obj.get_total_games()

                        if total == 0:
                            conn.sendall("RECENT_DATA:EMPTY".encode())
                            continue

                        entries = []
                        count = min(5, total)

                        for i in range(total - 1, total - count - 1, -1):
                            session = user_obj.get_history("game", i)
                            if session:
                                # reverse lookup index from name
                                g_idx = None
                                for key, val in self.game_map.items():
                                    if val == session.game_name:
                                        g_idx = key
                                        break

                                if g_idx is not None:
                                    entries.append(g_idx)
                        # send as CSV
                        conn.sendall(f"RECENT_DATA:{','.join(entries)}".encode())
            except Exception as e:
                print(f"[!] Server Error: {e}")
                break

        conn.close()
        with self.chat_lock:
            self.chat_clients = [
            (c, u) for (c, u) in self.chat_clients if c != conn
            ]


if __name__ == "__main__":
    ArcadeServer().start()