# How do I create a basic Python server?

Building a basic Python server is surprisingly easy because Python comes with built-in modules for it. Depending on whether you want a simple file server or a custom application server, there are two main approaches.

---

# 1. The "I just need it now" method (no code)

If you just want to serve files from a folder on your computer:

## Steps

Open your terminal or command prompt  
Navigate to the folder you want to serve  
Run:

```bash
python -m http.server 8000
```

Open your browser and go to:

http://localhost:8000

## What this does

Python starts a simple HTTP server that maps your folder structure to URLs.

---

# 2. The "I want to build an app" method (Flask)

If you want custom behavior like APIs or responses, use Flask.

## Step A: Install Flask

```bash
pip install flask
```

## Step B: Create app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, World!</h1><p>My Python server is running.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Step C: Run it

```bash
python app.py
```

Then go to:

http://localhost:5000

---

# Key Concepts

| Component | Description |
|----------|-------------|
| IP Address | 127.0.0.1 (this computer) |
| Hostname | localhost |
| Port | 8000 / 5000 etc. |

---

# Important note

These servers are NOT production-ready.

Use:
- Nginx  
- Gunicorn  
- uWSGI  

for real deployments.

---

# Arcade Server (Sockets)

For games, menus, and real-time control, use sockets instead of Flask.

---

# Why sockets?

Flask = request/response (disconnects)  
Sockets = persistent real-time connection  

---

# Comparison

| Feature | Flask | Sockets |
|--------|------|--------|
| Type | HTTP | TCP |
| Connection | Temporary | Persistent |
| Best for | Websites | Games / real-time apps |

---

# Basic socket server

```python
import socket
import threading

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    conn.sendall(b"Welcome to the Arcade!\n1. Play\n2. Exit\nChoose: ")

    while True:
        try:
            data = conn.recv(1024).decode().strip()

            if not data or data == "2":
                break

            if data == "1":
                conn.sendall(b"Guess 1-10: ")
                guess = conn.recv(1024).decode().strip()

                if guess == "7":
                    conn.sendall(b"YOU WIN!\n")
                else:
                    conn.sendall(b"WRONG!\n")
            else:
                conn.sendall(b"Invalid option\n")

        except:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 65432))
    server.listen()

    print("Server running...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
```

---

# Connect to server

```bash
nc localhost 65432
```

or

```bash
telnet localhost 65432
```

---

# Game idea expansion

- Server sends game state (JSON / strings)
- Client renders graphics (Tkinter / Pygame)
- Client sends input commands

Example:

x:10,y:20

---

# Simple state system

```python
state = "MENU"

if state == "MENU":
    if command == "START":
        state = "IN_GAME"
```

---

# Summary

Flask = web server  
Sockets = real-time arcade system
```
