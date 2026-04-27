"""
chat_message.py - Persistent chat message stored on a user's chat history.

Revision History:
    (ST) 04/26/2026 Create initial class
"""

from datetime import datetime


class ChatMessage:
    def __init__(self, sender, text, game_id="", timestamp=None):
        self.sender = sender
        self.text = text
        self.game_id = game_id
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        ts = self.timestamp.strftime("%H:%M")
        prefix = f"[{self.game_id}] " if self.game_id else ""
        return f"{prefix}[{ts}] {self.sender}: {self.text}"
