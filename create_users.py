"""
This program generates synthetic user data and leaderboard entries for the
ECE3822 arcade project. It writes users.dat and leaderboards.pkl so the
server and client can load a realistic pre-populated dataset.

Revision History:
    (ST) 04/30/2026 Create initial program
"""

import sys
import os
import random
import pickle
from datetime import datetime, timedelta
from faker import Faker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_interaction.user import User
from user_interaction.chat_message import ChatMessage
from game_interaction.game_session import GameSession
from game_interaction.leaderboard import Leaderboard
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
from algorithms.merge_sort import MergeSort
from user_interaction.chat_moderation import PrimeHashTable

fake = Faker()
Faker.seed(42)
random.seed(42)

# set to 1_000 for a quick test run
TARGET_USERS    = 10_000
TARGET_SESSIONS = 100_000  # total game sessions across all users
CHAT_MIN        = 10
CHAT_MAX        = 100
# 100k users produces several GB of pickle files and ~30 min generation time

# word pools for username generation
adjectives = [
    'cool', 'swift', 'silent', 'brave', 'clever', 'mighty', 'lucky',
    'sneaky', 'wild', 'fuzzy', 'epic', 'shadow', 'cosmic', 'fierce',
    'noble', 'rapid', 'mystic', 'frozen', 'golden', 'crimson',
    'dark', 'neon', 'toxic', 'hyper', 'turbo', 'blaze', 'storm',
    'steel', 'alpha', 'omega', 'phantom', 'cyber', 'solar', 'lunar',
    'iron', 'quantum', 'rogue', 'ultra', 'nitro', 'savage', 'blazing',
    'electric', 'frosty', 'gloom', 'jade', 'silver', 'copper', 'void',
    'radiant', 'stealth', 'wicked', 'chrome', 'primal', 'lethal',
    'venomous', 'ancient', 'divine', 'hollow', 'scarlet', 'azure',
    'obsidian', 'emerald', 'thunder', 'infernal', 'spectral', 'arcane',
]

nouns = [
    'tiger', 'wizard', 'ninja', 'panda', 'falcon', 'dragon', 'phoenix',
    'wolf', 'raven', 'shark', 'hawk', 'fox', 'bear', 'eagle', 'lion',
    'panther', 'viper', 'otter', 'lynx', 'badger',
    'cobra', 'scorpion', 'mantis', 'hydra', 'kraken', 'golem',
    'specter', 'wraith', 'titan', 'saber', 'blade', 'arrow', 'comet',
    'pulse', 'cipher', 'nova', 'ghost', 'reaper', 'hunter', 'striker',
    'ranger', 'knight', 'rogue', 'mage', 'bard', 'paladin', 'monk',
    'samurai', 'pirate', 'outlaw', 'bandit', 'rebel', 'nomad',
    'oracle', 'spirit', 'speeder', 'warden', 'sentinel', 'paragon',
    'apex', 'vector', 'nexus', 'signal', 'tempest', 'flux',
]

# game id to name mapping, must match main_server.py
GAME_MAP = {
    "0": "LUAIANID",
    "1": "JAG",
    "2": "VERMIS",
    "3": "RICHARD",
    "4": "TOM",
}

GAME_GENRES = {
    "LUAIANID": "puzzle",
    "JAG":      "action",
    "VERMIS":   "arcade",
    "RICHARD":  "rpg",
    "TOM":      "platformer",
}

# (mean, std, min, max) — all scores capped at 500
GAME_SCORE_PARAMS = {
    "LUAIANID": (150, 100,  5, 500),
    "JAG":      (130,  90,  5, 500),
    "VERMIS":   (200, 120, 10, 500),
    "RICHARD":  (170, 110, 10, 500),
    "TOM":      (160, 100,  5, 500),
}

# session timestamps fall within this window
SESSION_START     = datetime(2025, 1, 1)
SESSION_END       = datetime(2026, 4, 28)
SESSION_RANGE_SEC = int((SESSION_END - SESSION_START).total_seconds())

# session duration in seconds: gaussian around 12 minutes
DURATION_MEAN = 12 * 60
DURATION_STD  = 8  * 60
DURATION_MIN  = 2  * 60
DURATION_MAX  = 60 * 60

# short reactions that faker cannot generate more naturally
_REACTIONS = [
    "gg", "nice!", "lol", "wow", "ez", "gg wp", "nooo", "let's go!",
    "so close!", "haha", "oof", "rip", "bruh", "yooo", "what?!",
    "insane", "nope", "finally!", "again?", ":)", "wait what",
]

# {score}, {n}, {word} are filled at runtime by _fill()
_TEMPLATES = {
    "LUAIANID": [
        "just cracked level {n}, took forever",
        "hint for the {word} part?",
        "finally beat the {word} puzzle!",
        "scored {score} on the timed run",
        "the pattern is {word} then {word}",
        "level {n} is way harder than {n} was",
    ],
    "JAG": [
        "dodge {word} on the second phase",
        "just pulled off a {word} combo",
        "the {word} boss is weak to {word}",
        "scored {score} with the shotgun only",
        "you can skip the {word} room entirely",
        "that ambush at {word} caught me off guard",
    ],
    "VERMIS": [
        "just hit {score}, new pb!",
        "how do you handle the {word} turn?",
        "died at {score} again ugh",
        "the speed ramp after {score} is brutal",
        "going for {score} tonight",
        "sub {n} minute clear on my last run",
    ],
    "RICHARD": [
        "the {word} staff is op early game",
        "which quest gives {word} xp?",
        "the {word} boss dropped {word} gear",
        "running a full {word} build this time",
        "found a secret near the {word}",
        "save your {word} potions for floor {n}",
    ],
    "TOM": [
        "the {word} jump is impossible",
        "shortcut found at the {word} section",
        "world {n} is a huge difficulty spike",
        "my best time on world {n} is {n}:{n:02d}",
        "you can clip through {word} if you dash",
        "the hidden star in world {n} took me ages",
    ],
}


def _fill(template):
    """
    Fill a chat template with random score, level number, and faker word
    """
    return template.format(
        score=random.randint(0, 500),
        n=random.randint(1, 20),
        word=fake.word(),
    )


def random_chat_message(sender, game_id):
    """
    Generate a single chat message for the given sender and game.
    Uses a mix of short reactions, faker sentences, game templates, and catch phrases.
    Bypasses rate limiting and moderation since this is historical replay data.
    """
    roll = random.random()
    if roll < 0.12:
        text = random.choice(_REACTIONS)
    elif roll < 0.35:
        # faker sentence — may not be gaming-specific, that is acceptable
        text = fake.sentence(nb_words=random.randint(3, 9))
    elif roll < 0.60:
        text = _fill(random.choice(_TEMPLATES[game_id]))
    elif roll < 0.75:
        text = f"just got {random.randint(0, 500):,} {fake.word()}"
    else:
        text = fake.catch_phrase() if random.random() < 0.5 else fake.bs()
    offset = random.randint(0, SESSION_RANGE_SEC)
    ts = SESSION_START + timedelta(seconds=offset)
    return ChatMessage(sender, text, game_id=game_id, timestamp=ts,
                       moderated=False, rate_limited=False)


def make_usernames(n):
    """
    Generate n unique usernames using four styles:
    adjective+Noun+number, firstname+number, firstname_lastname, adjective_noun.
    PrimeHashTable keeps capacity prime so quadratic probing covers all slots.
    """
    seen  = PrimeHashTable(initial_capacity=n * 2)
    count = 0
    while count < n:
        style = random.randint(0, 3)
        if style == 0:
            u = f"{random.choice(adjectives)}{random.choice(nouns).capitalize()}{random.randint(1, 9999)}"
        elif style == 1:
            u = f"{fake.first_name().lower()}{random.randint(1, 9999)}"
        elif style == 2:
            u = f"{fake.first_name().lower()}_{fake.last_name().lower()}"
        else:
            u = f"{random.choice(adjectives)}_{random.choice(nouns)}"
        if u not in seen:
            seen.set(u, True)
            count += 1
    result = ArrayList()
    for entry in seen.items():
        result.append(entry[0])
    return result


# word pool for password generation
_pw_words = [
    'sun', 'moon', 'fire', 'ice', 'key', 'lock', 'run', 'jump',
    'red', 'blue', 'cat', 'dog', 'sky', 'sea', 'star', 'rock',
]


def random_password():
    """
    Generate a random password using one of three patterns:
    word+number, firstname+number+symbol, or word_word+number
    """
    style = random.randint(0, 2)
    if style == 0:
        return f"{random.choice(_pw_words)}{random.randint(100, 9999)}"
    elif style == 1:
        return f"{fake.first_name().lower()}{random.randint(10, 999)}!"
    else:
        return f"{random.choice(_pw_words)}_{random.choice(_pw_words)}{random.randint(1, 99)}"


def gaussian_score(game_name):
    """
    Return a score sampled from the gaussian distribution for the given game,
    clamped to [min, max] from GAME_SCORE_PARAMS
    """
    mean, std, lo, hi = GAME_SCORE_PARAMS[game_name]
    return max(lo, min(hi, int(random.gauss(mean, std))))


def random_session_times():
    """
    Return a (start, end) datetime pair within the session window.
    Duration is gaussian around 12 minutes, clamped to [2, 60] minutes.
    """
    offset   = random.randint(0, SESSION_RANGE_SEC)
    start    = SESSION_START + timedelta(seconds=offset)
    duration = max(DURATION_MIN, min(DURATION_MAX,
                   int(random.gauss(DURATION_MEAN, DURATION_STD))))
    end      = min(start + timedelta(seconds=duration), SESSION_END)
    return start, end


def make_session(user, game_name, score, start_time, end_time):
    """
    Build a GameSession with the given values and push it onto the user's play history.
    Bypasses end_session() to avoid resetting the score to zero.
    """
    sess            = GameSession(user, game_name)
    sess.score      = score
    sess.start_time = start_time
    sess.end_time   = end_time
    user.update_history("game", sess)


# weights order matches GAME_MAP key order: LUAIANID, JAG, VERMIS, RICHARD, TOM
GAME_WEIGHTS = [0.12, 0.22, 0.28, 0.20, 0.18]
game_names   = list(GAME_MAP.values())
REVERSE_MAP  = {v: k for k, v in GAME_MAP.items()}

leaderboards = {gid: Leaderboard() for gid in GAME_MAP}
users_array  = ArrayList()

print(f"Generating {TARGET_USERS:,} usernames ...")
usernames = make_usernames(TARGET_USERS)

# distribute exactly TARGET_SESSIONS across users using exponential weights
# so most users are casual and a few are heavy players
raw_counts = ArrayList()
for _ in range(TARGET_USERS):
    raw_counts.append(max(1, int(random.expovariate(TARGET_USERS / TARGET_SESSIONS))))

total_raw = 0
for j in range(len(raw_counts)):
    total_raw += raw_counts[j]

# scale raw counts to sum exactly to TARGET_SESSIONS
session_counts = ArrayList()
for j in range(len(raw_counts)):
    session_counts.append(max(1, round(raw_counts[j] * TARGET_SESSIONS / total_raw)))

# fix any rounding error so the total is exact
diff = TARGET_SESSIONS
for j in range(len(session_counts)):
    diff -= session_counts[j]
for j in range(abs(diff)):
    idx = j % TARGET_USERS
    if diff > 0:
        session_counts[idx] += 1
    elif session_counts[idx] > 1:
        session_counts[idx] -= 1

print(f"Creating {TARGET_USERS:,} users ({TARGET_SESSIONS:,} total sessions) ...")
total_chats = 0

for i, uname in enumerate(usernames):
    user = User(uname, random_password())

    # assign sessions to games using weighted random, then group by game
    assigned    = random.choices(game_names, weights=GAME_WEIGHTS, k=session_counts[i])
    game_counts = HashTable()
    for gname in assigned:
        game_counts.set(gname, game_counts.get(gname, 0) + 1)

    game_items   = game_counts.items()
    played_games = ArrayList()
    for entry in game_items:
        played_games.append(entry[0])

    for entry in game_items:
        gname  = entry[0]
        n_sess = entry[1]
        gid    = REVERSE_MAP[gname]

        # collect session times then sort chronologically with MergeSort
        times = ArrayList()
        for _ in range(n_sess):
            times.append(random_session_times())
        for start, end in MergeSort(times):
            score = gaussian_score(gname)
            make_session(user, gname, score, start, end)
            user.record_play(GAME_GENRES[gname], gname, (end - start).total_seconds())
            leaderboards[gid].add_score(uname, float(score))

    # generate chat messages only for games this user actually played
    n_msgs    = random.randint(CHAT_MIN, CHAT_MAX)
    chat_pool = played_games if len(played_games) > 0 else game_names
    for _ in range(n_msgs):
        gname = random.choice(chat_pool)
        user.update_history("chat", random_chat_message(uname, gname))

    total_chats += n_msgs
    users_array.append(user)

    if (i + 1) % max(1, TARGET_USERS // 20) == 0:
        print(f"  {i + 1:>7,} / {TARGET_USERS:,} users created")

base       = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(base, "users.dat")
lb_file    = os.path.join(base, "leaderboards.pkl")

from user_interaction.user_storage import set_all_users
set_all_users(users_file, users_array)

with open(lb_file, "wb") as f:
    pickle.dump(leaderboards, f)

print(f"\nDone.")
print(f"  users.dat        -> {len(users_array):,} users | {total_chats:,} total chat messages")
for gid, gname in GAME_MAP.items():
    lb     = leaderboards[gid]
    scores = list(lb._user_scores.values())
    if scores:
        top     = lb.top_n(1)
        top_str = f"{top[0][0]} ({int(top[0][1])})" if top else "-"
        print(f"  {gname:<10} -> {len(scores):>6,} entries | "
              f"avg {int(sum(scores)/len(scores)):>6,} | top: {top_str}")
    else:
        print(f"  {gname:<10} ->      0 entries")
print(f"  leaderboards.pkl -> saved")
