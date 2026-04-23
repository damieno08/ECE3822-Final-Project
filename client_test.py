import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk

# Import your custom handlers
from user_interaction.user import User
from game_interaction.game_handler import Damien, Santiago, Paul, Richard

class ArcadeClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Networked Arcade")
        self.root.geometry("450x700")
        self.root.configure(bg="#1a1a1a")

        # Track the logged-in user object
        self.current_user = None
        
        # Mapping for easy instantiation
        self.handler_map = {
            0: Damien,
            1: Santiago,
            2: Paul,
            3: Richard
        }

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        self.show_login_screen()
        self.root.mainloop()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def connect_to_server(self):
        try:
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except:
            print("SYSTEM: Offline Mode")

    def receive_data(self):
        while True:
            try:
                message = self.s.recv(4096).decode()
                if message.startswith("SUCCESS:"):
                    # Extract name and create local user object
                    username = message.split(":")[1].strip()
                    self.current_user = User(username)
                    self.root.after(0, self.show_dashboard)
                
                elif message.startswith("USER_RESULTS:"):
                    res = message.split(":", 1)[1]
                    self.root.after(0, self.update_display, f"--- DB RESULTS ---\n{res}")
                
                elif message:
                    self.root.after(0, self.update_display, f"SRV: {message}")
            except: break

    # --- SCREENS ---

    def show_login_screen(self):
        self.clear_screen()
        self.current_user = None
        tk.Label(self.root, text="ARCADE ACCESS", fg="#00FF00", bg="#1a1a1a", font=("Courier", 24, "bold")).pack(pady=40)
        
        tk.Label(self.root, text="Username", fg="#00FF00", bg="#1a1a1a").pack()
        self.u_entry = tk.Entry(self.root, bg="#000", fg="#00FF00", insertbackground="white")
        self.u_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password", fg="#00FF00", bg="#1a1a1a").pack()
        self.p_entry = tk.Entry(self.root, bg="#000", fg="#00FF00", show="*", insertbackground="white")
        self.p_entry.pack(pady=5)
        
        tk.Button(self.root, text="CONNECT", command=self.attempt_login, bg="#333", fg="#00FF00", width=15).pack(pady=30)

    def attempt_login(self):
        user = self.u_entry.get().strip()
        if user:
            try:
                self.s.sendall(f"LOGIN_REQUEST:{user}".encode())
            except: pass

    def show_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"WELCOME, {self.current_user.name.upper()}", fg="#00FF00", bg="#1a1a1a", font=("Courier", 16)).pack(pady=40)
        
        tk.Button(self.root, text="USER LOOKUP", command=self.show_lookup_screen, bg="#333", fg="#00FF00", width=25, pady=10).pack(pady=10)
        tk.Button(self.root, text="GAME LOOKUP", command=self.show_game_search, bg="#333", fg="#00FF00", width=25, pady=10).pack(pady=10)
        tk.Button(self.root, text="LOGOUT", command=self.show_login_screen, bg="#440000", fg="white", width=10).pack(pady=20)

    def show_lookup_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="USER DATABASE", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18, "bold")).pack(pady=20)
        self.search_entry = tk.Entry(self.root, bg="#000", fg="#00FF00")
        self.search_entry.pack(pady=5)
        
        tk.Button(self.root, text="SEARCH", command=lambda: self.s.sendall(f"QUERY_USER:{self.search_entry.get()}".encode()), bg="#00FF00").pack(pady=5)
        self.display = tk.Text(self.root, state='disabled', height=12, width=45, bg="#000", fg="#00FF00", font=("Courier", 9))
        self.display.pack(pady=15)
        tk.Button(self.root, text="BACK", command=self.show_dashboard, bg="#333", fg="#00FF00").pack()

    def show_game_search(self):
        self.clear_screen()
        tk.Label(self.root, text="SELECT GAME", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18, "bold")).pack(pady=10)

        container = tk.Frame(self.root, bg="#1a1a1a")
        container.pack(fill="both", expand=True, padx=10, pady=5)
        canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.logo_images = []
        # Game display mapping
        game_data = [
            ("Luainid", 0, "game_interaction/games/game_damien/graphics/logo.png"), 
            ("Santiago", 1, "game_interaction/games/game_santiago/graphics/logo.png"), 
            ("Vermis", 2, "game_interaction/games/game_paul/graphics/logo.png"), 
            ("Richard", 3, "game_interaction/games/game_richard/graphics/logo.png"),
        ]

        for name, idx, path in game_data:
            try:
                img = ImageTk.PhotoImage(Image.open(path).resize((64, 64), Image.Resampling.LANCZOS))
            except:
                img = ImageTk.PhotoImage(Image.new('RGBA', (64, 64), (0,0,0,0)))
            
            self.logo_images.append(img)
            tk.Button(scrollable_frame, text=f"  {name.upper()}", image=img, compound="left",
                      command=lambda n=name, i=idx: self.show_play_screen(n, i),
                      bg="#000", fg="#00FF00", font=("Courier", 12, "bold"), anchor="w", 
                      padx=15, pady=8, relief="flat", bd=0).pack(fill="x", expand=True, pady=2)

        tk.Button(self.root, text="BACK", command=self.show_dashboard, bg="#333", fg="#00FF00").pack(pady=10)

    def show_play_screen(self, name, idx):
        self.clear_screen()
        tk.Label(self.root, text=f"READY: {name}", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18, "bold")).pack(pady=40)
        self.display = tk.Text(self.root, state='disabled', height=8, width=40, bg="#000", fg="#00FF00")
        self.display.pack(pady=10)
        
        # The Play button triggers the run_game with the specific index
        tk.Button(self.root, text="PLAY", command=lambda: Thread(target=self.run_game, args=(idx,), daemon=True).start(),
                  bg="#00FF00", fg="#000", font=("Courier", 14, "bold"), width=15).pack(pady=20)
        tk.Button(self.root, text="BACK", command=self.show_game_search, bg="#333", fg="#00FF00").pack()

    def run_game(self, idx):
        try:
            self.s.sendall(f"CLIENT_RUNNING_GAME_{idx}".encode())
            # Instantiate the specific handler with the current user object
            handler_class = self.handler_map[idx]
            game_instance = handler_class(self.current_user)
            
            # Start and get results
            time_played, score = game_instance.start_game()
            
            msg = f"GAME OVER\nTIME: {time_played}s\nSCORE: {score}"
            self.root.after(0, self.update_display, msg)
        except Exception as e:
            self.root.after(0, self.update_display, f"ERROR: {e}")

    def update_display(self, text):
        if hasattr(self, 'display'):
            self.display.config(state='normal')
            self.display.insert(tk.END, text + "\n")
            self.display.config(state='disabled')
            self.display.see(tk.END)

if __name__ == "__main__":
    ArcadeClient()