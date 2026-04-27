"""
chat.py - In-game chat showing last 20 messages (CircularBuffer).

Revision History:
    (ST) 04/24/2026 Create initial class
"""

from datastructures.circular_buffer import CircularBuffer


class Chat(CircularBuffer):

    MAX_MESSAGES = 20

    def __init__(self):
        super().__init__(capacity=Chat.MAX_MESSAGES)

    def send(self, user, message):
        """Write a formatted message into the buffer, evicting the oldest if full."""
        self.write(f"{user}: {message}")

    def send_message(self, chat_msg):
        """Accept a ChatMessage object and write its display string into the buffer."""
        self.write(str(chat_msg))

    def recent(self):
        """Return all stored messages in order from oldest to most recent."""
        result = []
        for i in range(self._size):
            idx = (self._head + i) % self._capacity
            result.append(self._buffer[idx])
        return result
