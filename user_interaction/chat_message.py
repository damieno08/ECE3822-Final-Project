"""
chat_message.py - Persistent chat message stored on a user's chat history.

Revision History:
    (ST) 04/26/2026 Create initial class
    (ST) 04/27/2026 Add moderation via ProfanityFilter
    (ST) 04/29/2026 Add per-player rate limiting via RateLimiter
"""

from datetime import datetime
from user_interaction.chat_moderation import _filter, _rate_limiter


class ChatMessage:
    def __init__(self, sender, text, game_id="", timestamp=None, moderated=True, rate_limited=True):
        self.sender = sender
        self.game_id = game_id
        self.timestamp = timestamp or datetime.now()

        # Rate limit check — skipped for replayed/stored messages (rate_limited=False)
        self.was_blocked = rate_limited and not _rate_limiter.is_allowed(sender)

        if self.was_blocked:
            self.text = text
            self.was_censored = False
        else:
            self.text = _filter.censor(text) if moderated else text
            self.was_censored = moderated and (self.text != text)

    def __str__(self):
        ts = self.timestamp.strftime("%H:%M")
        prefix = f"[{self.game_id}] " if self.game_id else ""
        return f"{prefix}[{ts}] {self.sender}: {self.text}"
