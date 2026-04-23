import socket
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from PIL import Image, ImageTk

# Import your specific structures
from user_interaction.user import User
from game_interaction.game_handler import Damien, Santiago, Paul, Richard

class ArcadeClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arcade Terminal")
        self.root.geometry("450x700")
        self.root.configure(bg="#1a1a1a")

        self.current_user = None
        self.handler_map = {0: Damien, 1: Santiago, 2: Paul, 3: Richard}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        self.show_login_screen()
        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.s.connect(('127.0.0.1', 65432))
            Thread(target=self.receive_data, daemon=True).start()
        except:
            print("System running in offline mode.")

    def receive_data(self):
        while True:
            try:
                message = self.s.recv(4096).decode()
                if not message: break

                if message.startswith("SUCCESS:"):
                    username = message.split(":")[1]
                    self.current_user = User(username, "session_active")
                    self.root.after(0, self.show_dashboard)
                
                elif message.startswith("ERROR:"):
                    err = message.split(":", 1)[1]
                    self.root.after(0, lambda m=err: messagebox.showerror("Login Failed", m))
                
                elif message.startswith("USER_RESULTS:"):
                    res = message.split(":", 1)[1]
                    # CHANGE: Use update_display with 'True' to clear previous search
                    self.root.after(0, lambda: self.update_display(f"--- LATEST SEARCH ---\n{res}", clear=True))
            except: break

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- SHARED UI LOGIC ---

    def update_display(self, text, clear=False):
        """
        Updates the text box. If clear is True, it deletes previous content.
        """
        if hasattr(self, 'display'):
            self.display.config(state='normal')
            if clear:
                self.display.delete('1.0', tk.END) # Clear existing text
            self.display.insert(tk.END, text + "\n")
            self.display.config(state='disabled')
            self.display.see(tk.END)

    # --- SCREENS ---

    def show_login_screen(self):
        self.clear_screen()
        self.current_user = None
        tk.Label(self.root, text="ARCADE ACCESS", fg="#00FF00", bg="#1a1a1a", font=("Courier", 24, "bold")).pack(pady=40)
        tk.Label(self.root, text="USERNAME", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12, "bold")).pack(pady=40)
        self.u_entry = tk.Entry(self.root, bg="black", fg="#00FF00", insertbackground="white")
        self.u_entry.pack(pady=5)
        tk.Label(self.root, text="PASSWORD", fg="#00FF00", bg="#1a1a1a", font=("Courier", 12, "bold")).pack(pady=40)
        self.p_entry = tk.Entry(self.root, bg="black", fg="#00FF00", show="*", insertbackground="white")
        self.p_entry.pack(pady=5)
        tk.Button(self.root, text="CONNECT", command=self.attempt_login, bg="#333", fg="#00FF00", width=15).pack(pady=30)

    def attempt_login(self):
        u, p = self.u_entry.get().strip(), self.p_entry.get().strip()
        if u and p:
            try: self.s.sendall(f"LOGIN_REQUEST:{u}:{p}".encode())
            except: messagebox.showerror("Error", "Server connection lost.")

    def show_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"LOGGED IN: {self.current_user.name.upper()}", 
                 fg="#00FF00", bg="#1a1a1a", font=("Courier", 14)).pack(pady=30)
        tk.Button(self.root, text="LOOKUP USERS", command=self.show_lookup, bg="#333", fg="#00FF00", width=25, pady=10).pack(pady=10)
        tk.Button(self.root, text="GAME SELECT", command=self.show_game_search, bg="#333", fg="#00FF00", width=25, pady=10).pack(pady=10)
        tk.Button(self.root, text="LOGOUT", command=self.show_login_screen, bg="#440000", fg="white").pack(side="bottom", pady=20)

    def send_query(self):
        """
        Sends the search query, then clears the input box immediately.
        """
        search_term = self.search_entry.get().strip()
        if search_term:
            self.s.sendall(f"QUERY_USER:{search_term}".encode())
            self.search_entry.delete(0, tk.END) # CHANGE: Clears the search box

    def show_lookup(self):
        self.clear_screen()
        tk.Label(self.root, text="USER DATABASE", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18)).pack(pady=10)
        
        self.search_entry = tk.Entry(self.root, bg="black", fg="#00FF00", insertbackground="white")
        self.search_entry.pack(pady=5)
        
        # CHANGE: Calls send_query instead of sending directly
        tk.Button(self.root, text="QUERY", command=self.send_query, bg="#222", fg="#00FF00").pack(pady=5)
        
        self.display = tk.Text(self.root, height=12, width=45, bg="black", fg="#00FF00", font=("Courier", 9))
        self.display.pack(pady=10)
        
        tk.Button(self.root, text="BACK", command=self.show_dashboard).pack()

    def show_game_search(self):
        self.clear_screen()
        tk.Label(self.root, text="AVAILABLE GAMES", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18, "bold")).pack(pady=15)

        container = tk.Frame(self.root, bg="#1a1a1a")
        container.pack(fill="both", expand=True, padx=5)

        canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.logos = []
        games = [
            ("Luainid", 0, "game_interaction/games/game_damien/graphics/logo.png"), 
            ("Santiago", 1, "game_interaction/games/game_santiago/graphics/logo.png"), 
            ("Vermis", 2, "game_interaction/games/game_paul/graphics/logo.png"), 
            ("Richard", 3, "game_interaction/games/game_richard/graphics/logo.png")
        ]

        for name, idx, path in games:
            try:
                img = ImageTk.PhotoImage(Image.open(path).resize((80, 80)))
            except:
                img = ImageTk.PhotoImage(Image.new('RGBA', (80, 80), (0,0,0,0)))
            self.logos.append(img)
            
            tk.Button(scrollable_frame, text=f"   {name.upper()}", image=img, compound="left",
                      command=lambda n=name, i=idx: self.show_play(n, i),
                      bg="#111", fg="#00FF00", font=("Courier", 16, "bold"), 
                      anchor="w", relief="flat", bd=2, padx=20).pack(fill="x", pady=5, padx=10)

        tk.Button(self.root, text="BACK TO DASHBOARD", command=self.show_dashboard, 
                  bg="#333", fg="#00FF00", width=25).pack(pady=20)

    def show_play(self, name, idx):
        self.clear_screen()
        tk.Label(self.root, text=f"LAUNCH MODULE: {name}", fg="#00FF00", bg="#1a1a1a", font=("Courier", 18)).pack(pady=40)
        self.display = tk.Text(self.root, height=8, width=40, bg="black", fg="#00FF00")
        self.display.pack()
        # CHANGE: Run game and clear display logic is handled inside update_display if needed
        tk.Button(self.root, text="START GAME", command=lambda: Thread(target=self.run_game, args=(idx,), daemon=True).start(),
                  bg="#00FF00", fg="black", font=("Courier", 14, "bold"), width=15).pack(pady=20)
        tk.Button(self.root, text="BACK", command=self.show_game_search).pack()

    def run_game(self, idx):
        try:
            handler_class = self.handler_map[idx]
            game_instance = handler_class(self.current_user)
            # CHANGE: We can clear the text box before the game results pop up
            self.root.after(0, lambda: self.update_display("RUNNING MODULE...", clear=True))
            
            time_played, score = game_instance.start_game()
            self.root.after(0, lambda: self.update_display(f"SESSION COMPLETE\nTIME: {time_played}s\nSCORE: {score}", clear=True))
        except Exception as e:
            self.root.after(0, lambda: self.update_display(f"CRITICAL ERROR: {e}", clear=True))

if __name__ == "__main__":
    ArcadeClient()