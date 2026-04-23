import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk  # Requires: pip install Pillow
from game_interaction.game_handler import games

class ArcadeClient:
    def __init__(self, games_list):
        self.games = games_list 
        self.root = tk.Tk()
        self.root.title("Python Networked Arcade")
        
        # Default size, but now responsive to window scaling
        self.root.geometry("400x600")
        self.root.configure(bg="#1a1a1a")

        # Networking Setup
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        # Start at Login
        self.show_login_screen()
        self.root.mainloop()

    def clear_screen(self):
        """Wipes the window for the next screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # SCREEN 1: LOGIN
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="ARCADE LOGIN", fg="#00FF00", bg="#1a1a1a", 
                 font=("Courier", 20, "bold")).pack(pady=(40, 20))
        
        tk.Label(self.root, text="Username", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack()
        self.u_entry = tk.Entry(self.root, bg="#000", fg="#00FF00", insertbackground="white")
        self.u_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack()
        self.p_entry = tk.Entry(self.root, bg="#000", fg="#00FF00", show="*", insertbackground="white")
        self.p_entry.pack(pady=5)
        
        tk.Button(self.root, text="LOGIN", command=self.show_dashboard, 
                  bg="#333", fg="#00FF00", width=15, font=("Courier", 10, "bold")).pack(pady=30)

    # ==========================================
    # SCREEN 2: DASHBOARD
    # ==========================================
    def show_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="WELCOME OPERATOR", fg="#00FF00", bg="#1a1a1a", 
                 font=("Courier", 18, "bold")).pack(pady=40)

        tk.Button(self.root, text="LOOKUP USER", command=lambda: print("Lookup Active"),
                  bg="#333", fg="#00FF00", font=("Courier", 12), width=20, pady=10).pack(pady=10)

        tk.Button(self.root, text="SEARCH GAMES", command=self.show_game_search,
                  bg="#333", fg="#00FF00", font=("Courier", 12), width=20, pady=10).pack(pady=10)

    # ==========================================
    # SCREEN 3: SCROLLABLE GAME SEARCH
    # ==========================================
    def show_game_search(self):
        self.clear_screen()
        tk.Label(self.root, text="SELECT GAME", fg="#00FF00", bg="#1a1a1a", 
                 font=("Courier", 18, "bold")).pack(pady=10)

        # Container for scrollable area
        container = tk.Frame(self.root, bg="#1a1a1a")
        container.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

        # Sync scroll region
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window inside canvas and capture its ID for resizing
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Fullscreen support: Force the internal frame to match canvas width
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel binding
        self.root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.logo_images = []
        game_data = [
            ("Luainid", 0, "game_interaction/games/game_damien/graphics/logo.png"), 
            ("Santiago", 1, "game_interaction/games/game_santiago/graphics/logo.png"), 
            ("Vermis", 2, "game_interaction/games/game_paul/graphics/logo.png"), 
            ("Richard", 3, "game_interaction/games/game_richard/graphics/logo.png"),
        ]

        for name, idx, img_path in game_data:
            try:
                pil_img = Image.open(img_path)
                # Maintaining your 64x64 or slightly adjusting for list fit
                pil_img = pil_img.resize((64, 64), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_img) 
            except:
                # Transparent fallback
                img = ImageTk.PhotoImage(Image.new('RGBA', (64, 64), (0,0,0,0))) 
            
            self.logo_images.append(img)
            
            btn = tk.Button(
                scrollable_frame, 
                text=f"  {name.upper()}", 
                image=img,
                compound="left",
                command=lambda n=name, i=idx: self.show_play_screen(n, i),
                bg="#000", fg="#00FF00", 
                font=("Courier", 11, "bold"),
                anchor="w", padx=15, pady=5,
                activebackground="#00FF00",
                relief="flat", bd=0
            )
            # fill="x" and expand=True ensures the button stretches when window is maximized
            btn.pack(fill="x", expand=True, pady=2)

        tk.Button(self.root, text="RETURN", command=self.show_dashboard, 
                  bg="#333", fg="#00FF00", font=("Courier", 10)).pack(pady=10)

    # ==========================================
    # SCREEN 4: PLAY SCREEN
    # ==========================================
    def show_play_screen(self, game_name, game_idx):
        self.clear_screen()
        tk.Label(self.root, text=f"SYSTEM READY:\n{game_name}", fg="#00FF00", 
                 bg="#1a1a1a", font=("Courier", 18, "bold"), justify="center").pack(pady=40)
        
        self.display = tk.Text(self.root, state='disabled', height=8, width=35, 
                               bg="#000", fg="#00FF00", font=("Courier", 9))
        self.display.pack(pady=10)

        tk.Button(self.root, text=f"PLAY {game_name}", 
                  command=lambda: self.run_game_thread(game_idx),
                  bg="#00FF00", fg="#000", font=("Courier", 14, "bold"), 
                  width=20, pady=10).pack(pady=20)

        tk.Button(self.root, text="BACK TO SEARCH", command=self.show_game_search, 
                  bg="#333", fg="#00FF00", font=("Courier", 10)).pack()

    # ==========================================
    # LOGIC & NETWORKING
    # ==========================================
    def connect_to_server(self):
        try:
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except:
            print("SYSTEM: Offline Mode - Server Not Detected")

    def run_game_thread(self, game_idx):
        Thread(target=self.execute_game_logic, args=(game_idx,), daemon=True).start()

    def execute_game_logic(self, game_idx):
        try:
            msg = f"CLIENT_RUNNING_GAME_{game_idx}"
            self.s.sendall(msg.encode())
            played, score = self.games[game_idx].start_game()
            self.s.sendall(b"DISCONNECT")
            self.root.after(0, lambda: self.update_display(f"SESSION ENDED. SCORE: {score}"))
        except Exception as e:
            err_msg = str(e)
            self.root.after(0, lambda m=err_msg: self.update_display(f"SYSTEM ERROR: {m}"))

    def receive_data(self):
        while True:
            try:
                message = self.s.recv(1024).decode()
                if message:
                    self.root.after(0, lambda m=message: self.update_display(f"SRV: {m}"))
            except:
                break

    def update_display(self, text):
        if hasattr(self, 'display'):
            self.display.config(state='normal')
            self.display.insert(tk.END, text + "\n")
            self.display.config(state='disabled')
            self.display.see(tk.END)

if __name__ == "__main__":
    ArcadeClient(games)