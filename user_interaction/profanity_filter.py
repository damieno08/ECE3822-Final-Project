"""
profanity_filter.py - Chat moderation using a HashTable for O(1) word lookup.

Revision History:
    (ST) 04/26/2026 Create initial class
"""

import re
import os
from datastructures.hash_table import HashTable

_WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "profanity_wordlist.txt")

# Fallback list used only if the wordlist file is missing
_FALLBACK_LIST = [
    "damn", "hell", "crap", "ass", "asshole", "bastard", "bitch", "bullshit",
    "dick", "douche", "douchebag", "dumbass", "fuck", "fucking", "jackass",
    "motherfucker", "piss", "prick", "shit", "shithead", "slut", "twat",
    "whore", "wanker", "cunt", "cock", "fag", "faggot", "retard",
]


class ProfanityFilter:
    """
    Checks and censors profanity in chat messages using a HashTable.
    All lookups are O(1) average-case due to the backing hash table.

    Word list is loaded from profanity_wordlist.txt (one word per line).
    Falls back to a small built-in list if the file is not found.
    """

    def __init__(self, custom_words=None):
        self._table = HashTable()
        self._load_wordlist()
        if custom_words:
            for word in custom_words:
                self._table.set(word.lower(), True)

    def _load_wordlist(self):
        if os.path.exists(_WORDLIST_PATH):
            with open(_WORDLIST_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self._table.set(word, True)
        else:
            for word in _FALLBACK_LIST:
                self._table.set(word, True)

    def add_word(self, word):
        """Add a single word to the filter."""
        self._table.set(word.lower(), True)

    def remove_word(self, word):
        """Remove a single word from the filter."""
        self._table.delete(word.lower())

    def is_profane(self, word):
        """Return True if the word is in the profanity table."""
        return word.lower() in self._table

    def contains_profanity(self, text):
        """Return True if any word in text is profane."""
        for word in re.findall(r"[a-zA-Z]+", text):
            if self.is_profane(word):
                return True
        return False

    def censor(self, text):
        """Replace each profane word in text with asterisks of the same length."""
        def _replace(match):
            word = match.group()
            return "*" * len(word) if self.is_profane(word) else word

        return re.sub(r"[a-zA-Z]+", _replace, text)
