import socket
import tkinter as tk
import json
import pickle
import threading
import os
from tkinter import ttk, messagebox
from threading import Thread
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# Note: Ensure these local modules are in your directory
from user_interaction.user import User
from user_interaction.chat_message import ChatMessage
from user_interaction.user_storage import get_all_users, set_all_users, UserStorage
from game_interaction.game_handler import Damien, Santiago, Paul, Richard, Tom
from game_interaction.game_session import GameSession
from game_interaction.leaderboard import Leaderboard
from datastructures.array import ArrayList

# ============================================================
# CLIENT CODE
# ============================================================

class ArcadeClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FPGA ARCADE OS v1.0")
        self.root.geometry("550x850")
        self.root.configure(bg="#0d0d0d")
        
        self.colors = {
            "bg": "#0d0d0d",
            "fg": "#00ff41", 
            "accent": "#003b00",
            "header": "#008f11",
            "text_dim": "#004400"
        }

        self.game_metadata = {
            "0": ("LUAIANID", 0, "game_interaction/games/game_damien/graphics/logo.png"),
            "1": ("JAG_CORE", 1, "game_interaction/games/game_santiago/graphics/logo.png"),
            "2": ("VERMIS_V1", 2, "game_interaction/games/game_paul/graphics/logo.png"),
            "3": ("RICHARD_X", 3, "game_interaction/games/game_richard/graphics/logo.png"),
            "4": ("TOM_MOD", 4, "game_interaction/games/game_tom/graphics/logo.png")
        }

        self.current_user = None
        self.handler_map = {0: Damien, 1: Santiago, 2: Paul, 3: Richard, 4: Tom}
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.show_login_screen()
        self.root.mainloop()

    # ---------------- CONNECTION ----------------
    def connect_to_server(self):
        try:
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except:
            print("[!] SYSTEM_OFFLINE")

    def receive_data(self):
        while True:
            try:
                raw_data = self.s.recv(65536) 
                if not raw_data: break
                
                if raw_data.startswith(b"USER_PICKLE:"):
                    user_obj = pickle.loads(raw_data[len(b"USER_PICKLE:"):])
                    self.root.after(0, lambda: self.display_user_profile(user_obj))
                    continue

                msg = raw_data.decode('utf-8')
                if msg.startswith("SUCCESS:"):
                    self.current_user = User(msg.split(":")[1], "verified")
                    self.root.after(0, self.show_dashboard)
                elif msg.startswith("USER_RESULTS:"):
                    data = msg.split(":", 1)[1]
                    self.root.after(0, lambda: self.render_user_results(data))
                elif msg.startswith("LEADERBOARD_DATA:"):
                    data = msg.split(":", 1)[1]
                    self.root.after(0, lambda: self.render_leaderboard(data))
                elif msg.startswith("RECENT_DATA:"):
                    data = msg.split(":", 1)[1]
                    self.root.after(0, lambda d=data: self.render_recent_games(d))
            except: break

    # ---------------- UI HELPERS ----------------
    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def draw_separator(self, label_text):
        f = tk.Frame(self.root, bg=self.colors["bg"])
        f.pack(fill="x", padx=20, pady=(10, 2))
        tk.Label(f, text=f"[{label_text}]", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 9)).pack(side="left")
        tk.Frame(f, bg=self.colors["text_dim"], height=1).pack(side="left", fill="x", expand=True, padx=5)

    # ---------------- SCREENS ----------------
    def show_login_screen(self):
        self.clear()
        tk.Label(self.root, text="« FPGA_ARCADE »", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 26, "bold")).pack(pady=60)
        f = tk.Frame(self.root, bg="#000", padx=20, pady=20, highlightthickness=1, highlightbackground=self.colors["fg"])
        f.pack()
        tk.Label(f, text="LOGIN_ID:", fg=self.colors["fg"], bg="#000").pack()
        self.u_entry = tk.Entry(f, bg="#111", fg=self.colors["fg"], insertbackground=self.colors["fg"], bd=0); self.u_entry.pack(pady=5)
        tk.Label(f, text="ACCESS_CODE:", fg=self.colors["fg"], bg="#000").pack()
        self.p_entry = tk.Entry(f, bg="#111", fg=self.colors["fg"], show="*", insertbackground=self.colors["fg"], bd=0); self.p_entry.pack(pady=5)
        tk.Button(self.root, text="[ INITIALIZE ]", bg=self.colors["bg"], fg=self.colors["fg"], font=("Courier", 12, "bold"),
                  command=lambda: self.s.sendall(f"LOGIN_REQUEST|{self.u_entry.get()}|{self.p_entry.get()}".encode())).pack(pady=20)

    def show_dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"OPERATOR: {self.current_user.name.upper()}", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 14)).pack(pady=20)
        tk.Frame(self.root, bg=self.colors["fg"], height=2).pack(fill="x", padx=40)
        for txt, cmd in [("ACCESS GAME CORES", self.show_game_search), ("USER DATABASE", self.show_lookup), ("SHUTDOWN", self.root.quit)]:
            tk.Button(self.root, text=txt, fg=self.colors["fg"], bg="#111", width=25, font=("Courier", 11),
                      command=cmd, relief="flat", pady=10).pack(pady=15)

    # ---------------- GAME SELECTION ----------------
    def show_game_search(self):
        self.clear()
        tk.Label(self.root, text="— MODULE SELECTION —", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 16, "bold")).pack(pady=15)
        self.draw_separator("AVAILABLE CORES")
        self.all_logos = self.create_horizontal_scroll(self.root, list(self.game_metadata.values()))
        self.draw_separator("RECOMMENDED FOR YOU")
        recs = self.current_user.recommend()
        rec_data = []
        for name, _ in recs:
            found = next((v for v in self.game_metadata.values() if v[0].startswith(name.upper())), None)
            if found: rec_data.append(found)
        if not rec_data: rec_data = list(self.game_metadata.values())[:3]
        self.rec_logos = self.create_horizontal_scroll(self.root, rec_data)
        self.draw_separator("RECENT CACHE")
        self.recent_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.recent_container.pack(fill="x")
        self.s.sendall(f"GET_RECENTLY_PLAYED:{self.current_user.name}".encode())
        tk.Button(self.root, text="« RETURN", fg=self.colors["fg"], bg=self.colors["bg"], command=self.show_dashboard, relief="flat").pack(side="bottom", pady=10)

    def create_horizontal_scroll(self, parent, games):
        canvas = tk.Canvas(parent, bg=self.colors["bg"], height=125, highlightthickness=0)
        frame = tk.Frame(canvas, bg=self.colors["bg"])
        canvas.create_window((0, 0), window=frame, anchor="nw")
        logos = []
        for name, idx, path in games:
            try:
                img = ImageTk.PhotoImage(Image.open(path).resize((65, 65)))
            except:
                img = ImageTk.PhotoImage(Image.new('RGBA', (65, 65), (0, 255, 65, 20)))
            logos.append(img)
            b = tk.Button(frame, text=name, image=img, compound="top", bg="#000", fg=self.colors["fg"],
                          font=("Courier", 8), relief="flat", command=lambda i=idx: self.show_play(i))
            b.pack(side="left", padx=8, pady=5)
        canvas.pack(fill="x", padx=15)
        frame.update_idletasks(); canvas.config(scrollregion=canvas.bbox("all"))
        return logos

    def render_recent_games(self, data):
        for w in self.recent_container.winfo_children(): w.destroy()
        if data == "EMPTY":
            tk.Label(self.recent_container, text="CACHE EMPTY", fg=self.colors["text_dim"], bg=self.colors["bg"], font=("Courier", 10)).pack(pady=10)
            return
        games = [self.game_metadata[i] for i in data.split(",") if i in self.game_metadata]
        self.recent_logos = self.create_horizontal_scroll(self.recent_container, games)

    def show_play(self, idx):
        self.clear()
        name = self.game_metadata[str(idx)][0]
        tk.Label(self.root, text=f"CORE: {name}", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 18, "bold")).pack(pady=10)
        lb_frame = tk.Frame(self.root, bg="#000", highlightthickness=1, highlightbackground=self.colors["fg"])
        lb_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(lb_frame, text="RANK   OPERATOR       SCORE", fg="#000", bg=self.colors["fg"], font=("Courier", 10, "bold")).pack(fill="x")
        self.lb_display = tk.Text(lb_frame, bg="#000", fg=self.colors["fg"], font=("Courier", 11), bd=0, padx=10, pady=10)
        self.lb_display.pack(fill="both", expand=True)
        self.s.sendall(f"GET_LEADERBOARD:{idx}".encode())
        tk.Button(self.root, text="RUN MODULE", bg=self.colors["fg"], fg="#000", font=("Courier", 12, "bold"),
                  command=lambda: Thread(target=self.run_game, args=(idx,), daemon=True).start()).pack(pady=5)
        tk.Button(
        self.root,
        text="REFRESH LEADERBOARD",
        bg="#111",
        fg=self.colors["fg"],
        font=("Courier", 10, "bold"),
        command=lambda: self.s.sendall(f"GET_LEADERBOARD:{idx}".encode())
            ).pack(pady=5)
        tk.Button(self.root, text="CANCEL", bg="#222", fg=self.colors["fg"], command=self.show_game_search).pack(pady=5)

    def render_leaderboard(self, data):
        self.lb_display.config(state="normal"); self.lb_display.delete("1.0", tk.END)
        for i, line in enumerate(data.strip().split("\n")[:12]):
            if " - " in line:
                user, score = line.split(" - ")
                self.lb_display.insert(tk.END, f"{str(i+1).ljust(6)} {user.upper().ljust(14)} {score.rjust(8)}\n")
        self.lb_display.config(state="disabled")

    # ---------------- DATABASE LOOKUP ----------------
    def show_lookup(self):
        self.clear()
        tk.Label(self.root, text="— DB_USER_QUERY —", fg=self.colors["fg"], bg=self.colors["bg"], font=("Courier", 16, "bold")).pack(pady=15)
        search_f = tk.Frame(self.root, bg=self.colors["bg"])
        search_f.pack(pady=10)
        self.search_entry = tk.Entry(search_f, bg="#111", fg=self.colors["fg"], font=("Courier", 12))
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_f, text="SCAN", bg=self.colors["fg"], fg="#000", font=("Courier", 10, "bold"),
                  command=lambda: self.s.sendall(f"QUERY_USER:{self.search_entry.get()}".encode())).pack(side="left")
        res_frame = tk.Frame(self.root, bg="#000", highlightthickness=1, highlightbackground=self.colors["fg"])
        res_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(res_frame, text="   MATCHED OPERATORS (CLICK TO LOAD)", fg="#000", bg=self.colors["fg"], font=("Courier", 10, "bold"), anchor="w").pack(fill="x")
        self.display = tk.Text(res_frame, bg="#000", fg=self.colors["fg"], font=("Courier", 11), bd=0, padx=10, pady=10, cursor="hand2")
        self.display.pack(fill="both", expand=True)
        tk.Button(self.root, text="« BACK", bg="#222", fg=self.colors["fg"], command=self.show_dashboard).pack(pady=10)

    def render_user_results(self, data):
        self.display.config(state="normal"); self.display.delete("1.0", tk.END)
        for line in data.strip().split("\n"):
            if "NAME:" in line:
                name = line.split("NAME:")[1].strip()
                tag = f"tag_{name}"
                self.display.insert(tk.END, f" > ACCESS_PROFILE: {name.upper()}\n", tag)
                self.display.tag_config(tag, foreground=self.colors["fg"])
                self.display.tag_bind(tag, "<Button-1>", lambda e, n=name: self.s.sendall(f"GET_HISTORY:{n}".encode()))
        self.display.config(state="disabled")

    # ---------------- PROFILE & HISTORY ----------------
    def display_user_profile(self, user_obj):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)

        self.display.insert(tk.END, f"FILE: {user_obj.name.upper()}\n{'='*30}\n")
        self.display.insert(tk.END, f"TOTAL_SESSIONS: {user_obj.get_total_games()}\n")
        self.display.insert(tk.END, f"ACTIVE_TIME:    {user_obj.get_total_playtime()}s\n\n")

        self.display.insert(tk.END, "[ VIEW PLAY HISTORY ]\n", "play_btn")
        self.display.insert(tk.END, "[ VIEW CHAT HISTORY ]\n\n", "chat_btn")

        self.display.tag_config("play_btn", foreground=self.colors["fg"], font=("Courier", 11, "bold"))
        self.display.tag_config("chat_btn", foreground=self.colors["fg"], font=("Courier", 11, "bold"))

        self.display.tag_bind("play_btn", "<Button-1>", lambda e: self.load_play_history(user_obj))
        self.display.tag_bind("chat_btn", "<Button-1>", lambda e: self.load_chat_history(user_obj))
        self.display.config(state='disabled')

    def load_play_history(self, user_obj):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.insert(tk.END, f"[PLAY HISTORY: {user_obj.name.upper()}]\n{'='*30}\n\n")
        total = user_obj.get_total_games()
        if total == 0:
            self.display.insert(tk.END, "NO PLAY HISTORY FOUND\n")
        else:
            for i in range(total):
                game = user_obj.get_history('game', i)
                tag = f"game_{i}"
                self.display.insert(tk.END, f"▶ {game}\n", tag)
                self.display.tag_config(tag, foreground=self.colors["fg"])
                self.display.tag_bind(tag, "<Button-1>", lambda e, g=game: messagebox.showinfo("GAME ENTRY", str(g)))
        
        self.display.insert(tk.END, "\n[ BACK TO PROFILE ]", "back_p")
        self.display.tag_config("back_p", foreground=self.colors["fg"])
        self.display.tag_bind("back_p", "<Button-1>", lambda e: self.display_user_profile(user_obj))
        self.display.config(state='disabled')

    def load_chat_history(self, user_obj):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.insert(tk.END, f"[CHAT HISTORY: {user_obj.name.upper()}]\n{'='*30}\n\n")
        
        try:
            total = user_obj.chat_history.size()
            if total == 0:
                self.display.insert(tk.END, "NO CHAT HISTORY FOUND\n")
            else:
                for i in range(total):
                    msg = user_obj.get_history('chat', i)
                    tag = f"chat_{i}"
                    self.display.insert(tk.END, f" •{msg.game_id} {msg.text}\n", tag)
                    self.display.tag_config(tag, foreground=self.colors["fg"])
                    self.display.tag_bind(tag, "<Button-1>", lambda e, m=msg: messagebox.showinfo("CHAT ENTRY", str(m)))
        except:
            self.display.insert(tk.END, "ERROR LOADING CHAT DATAS\n")

        self.display.insert(tk.END, "\n[ BACK TO PROFILE ]", "back_p")
        self.display.tag_config("back_p", foreground=self.colors["fg"])
        self.display.tag_bind("back_p", "<Button-1>", lambda e: self.display_user_profile(user_obj))
        self.display.config(state='disabled')

    def run_game(self, idx):
        try:
            handler = self.handler_map[idx](self.current_user)

            duration, score, chat_log = handler.start_game()

            self.current_user.record_play(
                handler.genre,
                handler.name,
                duration.total_seconds()
            )

            # ---------------- SESSION SAVE ----------------
            self.s.sendall(
                f"SAVE_SESSION|{self.current_user.name}|{score}|{duration}|{idx}\n".encode()
            )
            if chat_log:
                for m in chat_log:
                    game_name = self.game_metadata[str(idx)][0]

                    msg = (
                        f"SAVE_CHAT|{self.current_user.name}|"
                        f"{game_name}|{m.sender}|{m.text}|"
                        f"{m.timestamp.isoformat() if m.timestamp else ''}\n"
                    )

                    self.s.sendall(msg.encode())

            # ---------------- UI RETURN (FIX) ----------------
            self.root.after(0, lambda: self.show_play(idx))

            messagebox.showinfo(
                "MODULE COMPLETE",
                f"SCORE: {score}\nTIME: {duration}"
            )

        except Exception as e:
            messagebox.showerror("GAME ERROR", str(e))


if __name__ == "__main__":
    # Choose to run Client or Server
    ArcadeClient() 
