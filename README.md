# ECE3822 Final Project — Arcade Terminal

A networked arcade launcher with a graphical login client, a user account server, and four Pygame games.

---

## Installing Python

Go to https://www.python.org/downloads/ and download the latest **Python 3.10+** installer for Windows. Run the installer and make sure to check **"Add Python to PATH"** on the first screen before clicking Install.

Verify it worked by opening a terminal and running:

```
python --version
```

---

## Installing Required Libraries

This project requires two libraries that do not come with Python. Run these commands in your terminal:

```
pip install pygame
pip install Pillow
```

---

## Opening the Project

Open your terminal and navigate to the project folder:

```
cd C:\ece-3822\ECE3822-Final-Project
```

All commands below must be run from inside this folder.

---

## Running the Program

The project has two parts that must run at the same time in **two separate terminal windows**, both opened to the project folder.

### Server

```
python main_server.py
```

Leave this terminal open. It handles user accounts and login. Press `Ctrl+C` to shut it down when you're done. User data is automatically saved to `users.dat` on shutdown.

### Client

```
python client_test.py
```

A green-on-black **Arcade Terminal** window will open.

---

## Using the Application

### Login

Enter any username and password, then click **CONNECT**. If the username is new, an account is automatically created. If it already exists, the password must match.

### Dashboard

After logging in you have two options:

- **Lookup Users** — search for registered users by name
- **Game Select** — pick and launch one of the four games

### Launching a Game

Select a game from the list and click **Start Game**. A Pygame window will open. When you close it, the terminal will show your time played and score.

---

## Notes

- Both terminals must stay open at the same time — the server must be running for login to work.
- The games require a display (Pygame), so this will not work over a remote/headless connection.
