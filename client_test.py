import socket
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from PIL import Image, ImageTk
from user_interaction.user import User
from game_interaction.game_handler import Damien, Santiago, Paul, Richard, Tom

class ArcadeClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arcade Terminal")
        self.root.geometry("450x700")
        self.root.configure(bg="#1a1a1a")
        self.current_user = None
        self.handler_map = {0: Damien, 1: Santiago, 2: Paul, 3: Richard, 4:Tom}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.show_login_screen()
        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except:
            print("[!] Connection Error")

    def receive_data(self):
        while True:
            try:
                msg = self.s.recv(4096).decode()
                if not msg:
                    break

                if msg.startswith("SUCCESS:"):
                    self.current_user = User(msg.split(":")[1], "verified")
                    self.root.after(0, self.show_dashboard)

                elif msg.startswith("ERROR:"):
                    err = msg.split(":", 1)[1]
                    self.root.after(0, lambda: messagebox.showerror("Login Error", err))

                elif msg.startswith("USER_RESULTS:"):
                    self.root.after(0, lambda: self.display_clickable_users(msg.split(":", 1)[1]))

                elif msg.startswith("HISTORY_DATA:"):
                    self.root.after(0, lambda: self.update_display(msg.split(":", 1)[1], clear=True))
                elif msg.startswith("LEADERBOARD_DATA:"):
                    self.root.after(0, lambda: self.update_display(msg.split(":", 1)[1], clear=True))
            except:
                break

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_display(self, text, clear=False):
        if hasattr(self, 'display'):
            self.display.config(state='normal')
            if clear:
                self.display.delete('1.0', tk.END)
            self.display.insert(tk.END, text + "\n")
            self.display.config(state='disabled')

    def display_clickable_users(self, data):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.insert(tk.END, "--- SEARCH RESULTS ---\n\n")

        for line in data.strip().split("\n"):
            if "NAME:" in line:
                name = line.split("NAME:")[1].strip()
                tag = f"tag_{name}"

                start = self.display.index(tk.INSERT)
                self.display.insert(tk.END, f" > {name.upper()}\n")

                self.display.tag_add(tag, start, self.display.index(tk.INSERT))
                self.display.tag_config(tag, foreground="#00FF00", font=("Courier", 10, "bold"))

                self.display.tag_bind(
                    tag,
                    "<Button-1>",
                    lambda e, n=name: self.s.sendall(f"GET_HISTORY:{n}".encode())
                )

        self.display.config(state='disabled')

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="FPGA Arcade", fg="#00FF00", bg="#1a1a1a", font=("Courier", 20)).pack(pady=40)
        tk.Label(self.root, text="Username", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack(pady=40)
        self.u_entry = tk.Entry(self.root, bg="black", fg="#00FF00")
        self.u_entry.pack(pady=5)
        tk.Label(self.root, text="Password", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack(pady=40)
        self.p_entry = tk.Entry(self.root, bg="black", fg="#00FF00", show="*")
        self.p_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="LOGIN",
            command=lambda: self.s.sendall(
                f"LOGIN_REQUEST|{self.u_entry.get()}|{self.p_entry.get()}".encode()
            )
        ).pack(pady=20)

        tk.Button(self.root, text="EXIT", bg="#440000", fg="white", command=self.root.quit).pack(pady=10)

    def show_dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text=f"WELCOME {self.current_user.name}", fg="#00FF00", bg="#1a1a1a").pack(pady=20)

        tk.Button(self.root, text="USER DATABASE", command=self.show_lookup, width=25).pack(pady=10)
        tk.Button(self.root, text="GAME SELECT", command=self.show_game_search, width=25).pack(pady=10)
        tk.Button(self.root, text="LOGOUT", command=self.show_login_screen, bg="#333", fg="white").pack(side="bottom", pady=20)

    def show_lookup(self):
        self.clear_screen()

        tk.Label(self.root, text="SEARCH USERS", fg="#00FF00", bg="#1a1a1a").pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        tk.Button(
            self.root,
            text="QUERY",
            command=lambda: self.s.sendall(f"QUERY_USER:{self.search_entry.get()}".encode())
        ).pack()

        self.display = tk.Text(self.root, height=15, width=45, bg="black", fg="#00FF00")
        self.display.pack()

        tk.Button(self.root, text="BACK", command=self.show_dashboard).pack()

    def show_game_search(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg="#1a1a1a")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, command=canvas.yview)

        scroll_frame = tk.Frame(canvas, bg="#1a1a1a")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=430)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.logos = []

        games = [
            ("Luaianid", 0, "game_interaction/games/game_damien/graphics/logo.png"),
            ("Santiago", 1, "game_interaction/games/game_santiago/graphics/logo.png"),
            ("Vermis", 2, "game_interaction/games/game_paul/graphics/logo.png"),
            ("Richard", 3, "game_interaction/games/game_richard/graphics/logo.png"),
            ("Tom", 4, "game_interaction/games/game_tom/graphics/logo.png")
        ]

        for name, idx, path in games:
            try:
                img = ImageTk.PhotoImage(Image.open(path).resize((70, 70)))
            except:
                img = ImageTk.PhotoImage(Image.new('RGBA', (70, 70)))

            self.logos.append(img)

            tk.Button(
                scroll_frame,
                text=f"  {name}",
                image=img,
                compound="left",
                anchor="w",
                command=lambda i=idx: self.show_play(i),
                bg="#222",
                fg="#00FF00"
            ).pack(fill="x", pady=2)

        tk.Button(self.root, text="BACK", command=self.show_dashboard).pack(pady=10)

    def show_play(self, idx):
        self.clear_screen()

        self.display = tk.Text(self.root, height=10, width=40, bg="black", fg="#00FF00")
        self.display.pack(pady=20)

        # ✅ Load leaderboard automatically
        self.s.sendall(f"GET_LEADERBOARD:{idx}".encode())

        tk.Button(
            self.root,
            text="START MODULE",
            command=lambda: Thread(target=self.run_game, args=(idx,), daemon=True).start(),
            bg="#00FF00"
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="REFRESH LEADERBOARD",
            command=lambda: self.s.sendall(f"GET_LEADERBOARD:{idx}".encode())
        ).pack(pady=5)

        tk.Button(self.root, text="BACK", command=self.show_game_search).pack()

    def run_game(self, idx):
        try:
            handler = self.handler_map[idx](self.current_user)
            duration, score = handler.start_game()

            self.s.sendall(
                f"SAVE_SESSION|{self.current_user.name}|{score}|{duration}|{idx}".encode()
            )

            self.root.after(
                0,
                lambda: self.update_display(f"COMPLETED\nSCORE: {score}\nTIME: {duration}", clear=True)
            )

        except Exception as e:
            self.root.after(0, lambda err=e: self.update_display(f"ERROR: {err}", clear=True))


if __name__ == "__main__":
    ArcadeClient()