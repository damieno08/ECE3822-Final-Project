"""
chat_message.py - Persistent chat message stored on a user's chat history.

Revision History:
    (ST) 04/26/2026 Create initial class
    (ST) 04/27/2026 Add moderation via ProfanityFilter
"""

from datetime import datetime
from user_interaction.profanity_filter import ProfanityFilter

_filter = ProfanityFilter()


class ChatMessage:
    def __init__(self, sender, text, game_id="", timestamp=None, moderated=True):
        self.sender = sender
        self.text = _filter.censor(text) if moderated else text
        self.game_id = game_id
        self.timestamp = timestamp or datetime.now()
        self.was_censored = moderated and (self.text != text)

    def __str__(self):
        ts = self.timestamp.strftime("%H:%M")
        prefix = f"[{self.game_id}] " if self.game_id else ""
        return f"{prefix}[{ts}] {self.sender}: {self.text}"
