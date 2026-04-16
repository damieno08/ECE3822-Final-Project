import socket
import tkinter as tk
from threading import Thread

from game_interaction.game import games

class ArcadeClient:
    def __init__(self, games_list):
        # This stores your list so the button can find it
        self.games = games_list 
        
        # --- GUI Setup ---
        self.root = tk.Tk()
        self.root.title("Python Networked Arcade")
        self.root.geometry("400x500")
        self.root.configure(bg="#1a1a1a")

        # Terminal Display
        self.display = tk.Text(
            self.root, 
            state='disabled', 
            height=15, 
            width=45, 
            bg="#000", 
            fg="#00FF00", # Classic Matrix Green
            insertbackground="white"
        )
        self.display.pack(padx=20, pady=20)

        # The Magic Button
        self.action_btn = tk.Button(
            self.root, 
            text="LAUNCH GAME [0]", 
            command=self.run_game_thread, # Calls the threader
            bg="#333",
            fg="#00FF00",
            font=("Courier", 12, "bold"),
            activebackground="#00FF00",
            padx=10,
            pady=5
        )
        self.action_btn.pack(pady=10)

        # --- Networking Setup ---
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Change 'localhost' to the Server's IP if playing on different PCs
            self.s.connect(('localhost', 65432))
            self.update_display("SYSTEM: Connected to Arcade Server.")
            
            # Background thread to listen for server messages
            Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            self.update_display(f"SYSTEM ERROR: Connection failed.\n{e}")

        self.root.mainloop()

    # ==========================================
    # GAME EXECUTION LOGIC
    # ==========================================
    def run_game_thread(self):
        """Starts the game in a separate thread to keep GUI alive."""
        game_thread = Thread(target=self.execute_game_logic, daemon=True)
        game_thread.start()

    def execute_game_logic(self):
        """The actual logic for calling your function."""
        try:
            self.update_display(">>> Requesting Game 0...")
            
            # 1. Notify the server you are starting
            self.s.sendall(b"NOTIFY: Starting Game 0")
            
            # 2. CALL YOUR FUNCTION
            # This is exactly what you requested:
            played,score = self.games[0].start_game()
            self.s.sendall(b"DISCONNECT")
            self.root.after(0, lambda: self.update_display(">>> Game session ended."))
            self.root.after(0, lambda: self.update_display(f"The game lasted {played}"))
            self.root.after(0, lambda: self.update_display(f"The game score was {score}"))

        except IndexError:
            self.update_display("ERROR: Game index 0 not found.")
        """
        except Exception as e:
            self.update_display(f"GAME ERROR: {e}")
        """

    # ==========================================
    # HELPER METHODS
    # ==========================================
    def receive_data(self):
        """Listens for data from the server."""
        while True:
            try:
                message = self.s.recv(1024).decode()
                if message:
                    self.update_display(f"SERVER: {message}")
            except:
                self.update_display("SYSTEM: Connection to server lost.")
                break

    def update_display(self, text):
        """Safely updates the text area."""
        self.display.config(state='normal')
        self.display.insert(tk.END, text + "\n")
        self.display.config(state='disabled')
        self.display.see(tk.END)

# ==========================================
# HOW TO RUN THIS
# ==========================================
if __name__ == "__main__":
    # 1. This represents your existing game setup
    class MyGame:
        def handle_game(self):
            # Your custom logic goes here!
            print("Game is running...") 

    # 2. Create your list of game objects 

    # 3. Start the client and pass the list in
    ArcadeClient(games)