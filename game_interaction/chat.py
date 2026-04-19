"""
chat.py - In-game chat showing last 20 messages (CircularBuffer).

Author: Santiago Troya
"""

from datastructures.circular_buffer import CircularBuffer


class Chat(CircularBuffer):

    MAX_MESSAGES = 20

    def __init__(self):
        super().__init__(capacity=Chat.MAX_MESSAGES)

    def send(self, user, message):
        pass

    def recent(self):
        pass
