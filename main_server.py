import socket
import threading
import pickle
import os
from datetime import datetime, timedelta

from user_interaction.user_storage import get_all_users, set_all_users, UserStorage
from user_interaction.user import User 
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
            "0": "Luaianid",
            "1": "Santiago",
            "2": "Vermis",
            "3": "Richard",
            "4": "Tom"
        }

        # ✅ Load or create leaderboards
        self.leaderboards = self.load_leaderboards()

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
        print(f"[*] Server Online at {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self.server.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
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
                raw_data = conn.recv(4096).decode()
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

                # ---------------- GET LEADERBOARD ----------------
                elif raw_data.startswith("GET_LEADERBOARD"):
                    g_idx = raw_data.split(":")[1].strip()

                    if g_idx in self.leaderboards:
                        lb = self.leaderboards[g_idx]
                        top = lb.top_n(10)

                        output = f"--- TOP PLAYERS ({self.game_map[g_idx]}) ---\n\n"
                        for i, (user, score) in enumerate(top, start=1):
                            output += f"{i}. {user} - {score}\n"

                        conn.sendall(f"LEADERBOARD_DATA:{output}".encode())

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

                # ---------------- GET HISTORY ----------------
                elif raw_data.startswith("GET_HISTORY:"):
                    target_name = raw_data.split(":")[1].strip()
                    user_obj = self.find_user_by_name(target_name)

                    if user_obj:
                        count = user_obj.get_total_games()
                        history_output = "" if count > 0 else "No play history found."

                        for i in range(count):
                            session = user_obj.get_history("game", i)
                            if session:
                                history_output += f"[{i+1}] {str(session)}\n"

                        conn.sendall(f"HISTORY_DATA:{history_output}".encode())

            except Exception as e:
                print(f"[!] Server Error: {e}")
                break

        conn.close()


if __name__ == "__main__":
    ArcadeServer().start()