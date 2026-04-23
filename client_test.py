import socket
import tkinter as tk
from threading import Thread
from game_interaction.game_handler import games

class ArcadeClient:
    def __init__(self, games_list):
        self.games = games_list 
        
        # --- GUI Setup ---
        self.root = tk.Tk()
        self.root.title("Python Networked Arcade")
        self.root.geometry("400x600")
        self.root.configure(bg="#1a1a1a")

        # Networking initialization (moved here so it connects immediately)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        # Start with the Login Screen
        self.show_login_screen()
        self.root.mainloop()

    def clear_screen(self):
        """Removes all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # SCREEN 1: LOGIN
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()

        # Logo Placeholder
        try:
            self.logo_img = tk.PhotoImage(file="") # Add path here
            logo_label = tk.Label(self.root, image=self.logo_img, bg="#1a1a1a")
            logo_label.pack(pady=20)
        except:
            tk.Label(self.root, text="ARCADE LOGIN", fg="#00FF00", bg="#1a1a1a", 
                     font=("Courier", 20, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username:", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack(pady=5)
        self.user_entry = tk.Entry(self.root, bg="#000", fg="#00FF00", insertbackground="white")
        self.user_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(self.root, show="*", bg="#000", fg="#00FF00", insertbackground="white")
        self.pass_entry.pack(pady=5)

        login_btn = tk.Button(
            self.root, text="ENTER", command=self.attempt_login,
            bg="#333", fg="#00FF00", font=("Courier", 12, "bold"),
            activebackground="#00FF00", width=15
        )
        login_btn.pack(pady=20)

    def attempt_login(self):
        # Basic logic: Check if fields aren't empty (Replace with server-side check if needed)
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if username:
            self.show_game_menu()

    # ==========================================
    # SCREEN 2: GAME MENU
    # ==========================================
    def show_game_menu(self):
        self.clear_screen()

        # Menu Logo
        try:
            self.menu_logo = tk.PhotoImage(file="") # Add path here
            tk.Label(self.root, image=self.menu_logo, bg="#1a1a1a").pack(pady=10)
        except:
            tk.Label(self.root, text="SELECT A GAME", fg="#00FF00", bg="#1a1a1a", 
                     font=("Courier", 18, "bold")).pack(pady=10)

        # Terminal Display (Integrated into menu)
        self.display = tk.Text(
            self.root, state='disabled', height=8, width=40, 
            bg="#000", fg="#00FF00"
        )
        self.display.pack(padx=20, pady=10)

        # Game Launch Buttons
        game_names = [("Luainid", 0), ("Santiago", 1), ("Vermis", 2), ("Richard", 3)]
        
        for name, idx in game_names:
            btn = tk.Button(
                self.root, text=f"LAUNCH {name}", 
                command=lambda i=idx: self.run_game_thread(i),
                bg="#333", fg="#00FF00", font=("Courier", 10, "bold"),
                activebackground="#00FF00", width=25, pady=5
            )
            btn.pack(pady=5)

    # ==========================================
    # CORE LOGIC & NETWORKING
    # ==========================================
    def connect_to_server(self):
        try:
            # Using '127.0.0.1' is often more reliable than 'localhost' on Linux
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            print(f"Connection failed: {e}")
            # Don't crash! Just let the user know via console or a popup later

    def run_game_thread(self, game_type):
        Thread(target=self.execute_game_logic, args=(game_type,), daemon=True).start()

    def execute_game_logic(self, game_type):
        try:
            self.root.after(0, lambda: self.update_display(f">>> Launching Game {game_type}..."))
            self.s.sendall(f"NOTIFY: Starting Game {game_type}".encode())
            
            played, score = self.games[game_type].start_game()
            
            self.s.sendall(b"DISCONNECT")
            self.root.after(0, lambda: self.update_display(f">>> Session Ended. Score: {score}"))
        except Exception as e:
            self.root.after(0, lambda err=e: self.update_display(f"GAME ERROR: {err}"))

    def receive_data(self):
        while True:
            try:
                message = self.s.recv(1024).decode()
                if message:
                    self.root.after(0, lambda m=message: self.update_display(f"SERVER: {m}"))
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