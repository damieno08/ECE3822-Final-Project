"""
profanity_filter.py - Chat moderation using a HashTable for O(1) word lookup.

Revision History:
    (ST) 04/26/2026 Create initial class
"""

import re
from datastructures.hash_table import HashTable


def _next_prime(n):
    """Return the smallest prime >= n."""
    def _is_prime(x):
        if x < 2:
            return False
        if x < 4:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True
    while not _is_prime(n):
        n += 1
    return n


class PrimeHashTable(HashTable):
    """
    HashTable subclass that keeps capacity at a prime number.
    This ensures quadratic probing covers ~half the table instead of
    cycling through only a small fixed set of offsets (the power-of-2 bug).
    """

    def __init__(self, initial_capacity=251):
        super().__init__(_next_prime(initial_capacity))

    def _resize(self):
        old_bins = self.bins
        self.capacity = _next_prime(self.capacity * 2)
        self.number_elements = 0
        from datastructures.array import ArrayList
        self.bins = ArrayList(self.capacity)
        for _ in range(self.capacity):
            self.bins.append(None)
        for i in range(len(old_bins)):
            entry = old_bins[i]
            if entry is not None:
                self.set(entry[0], entry[1])

#profanities imported from the github repository: "https://github.com/arhankundu99/profanity-filter/blob/master/data/profanity_wordlist.txt"


_PROFANITY_LIST = ["anal", "anus", "arse", "ass", "ballsack", "bastard", "bdsm", "bitch", "bimbo", "blowjob", "boob", "booobs", "breasts", "boner", "bondage", "bullshit", "busty", "butthole", "cawk", "chink", "clit", "cnut", "cock", "cokmuncher", "cowgirl", "crap", "crotch", "cum", "cunt", "damn", "dick", "dildo", "dink", "deepthroat", "doosh", "douche", "duche", "ejaculate", "ejaculating", "ejaculation", "ejakulate", "erotic", "erotism", "fag", "fatass", "femdom", "fingering", "footjob", "fuck", "fcuk", "fingerfuck", "fistfuck", "fook", "fooker", "fuk", "gangbang", "gaysex", "handjob", "hentai", "hooker", "hoer", "homo", "horny", "incest", "jackoff", "jerkoff", "jizz", "masturbate", "mofo", "mothafuck", "motherfuck", "milf", "muff", "nigga", "nigger", "nipple", "nob", "numbnuts", "nutsack", "nude", "orgy", "orgasm", "panty", "panties", "penis", "playboy", "porn", "pussy", "pussies", "rape", "raping", "rapist", "rectum", "retard", "rimming", "sadist", "sadism", "scrotum", "sex", "semen", "shemale", "shit", "slut", "spunk", "stripclub", "tit", "threesome", "throating", "twat", "viagra", "vagina", "wank", "whore", "whoar", "xxx"]


class ProfanityFilter:
    """
    Checks and censors profanity in chat messages using a HashTable.
    All lookups are O(1) average-case due to the backing hash table.

    Word list is loaded from profanity_wordlist.txt (one word per line).
    Falls back to a small built-in list if the file is not found.
    """

    def __init__(self, custom_words=None):
        self._table = PrimeHashTable()
        self._load_wordlist()
        if custom_words:
            for word in custom_words:
                self._table.set(word.lower(), True)

    def _load_wordlist(self):
        for word in _PROFANITY_LIST:
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
