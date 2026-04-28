"""
dialog_data.py - NPC dialog tree definitions

Author: Santiago Troya
Date:   04/27/2026
Lab:    Lab 7 - NPC Dialog with Graphs

NPCs are drawn from the Joker's Ascension game design (Lab 1):
  - Jack           : condescending gatekeeper at the Poker Table
  - King of Hearts : polite but unshakeable guardian of the Queen
  - Queen of Hearts: haughty, power-mad ruler of the Hall of Hearts (AI node)
"""

from game_interaction.games.game_santiago.code.game.dialog_graph import DialogGraph


# ---------------------------------------------------------------------------
# NPC 1 - Jack
# Personality (Lab 1): "Look below the shoulder type of guy" -- condescending,
# knows he is the gatekeeper between the player and the King.
# Features: branching, loop back to menu.
# ---------------------------------------------------------------------------

def _make_jack():
    dg = DialogGraph("Jack")

    dg.add_dialog_node(
        "greet",
        "Oh. It's you. A buffoon wandering into places above their station. "
        "What do you want? Make it quick, I'm busy."
    )
    dg.add_dialog_node(
        "menu",
        "Still here? Fine. Ask what you must, but don't waste my time."
    )
    dg.add_dialog_node(
        "about_king",
        "The King? Ha. He is polite, I'll give him that. But he will not move "
        "an inch for you. He has sworn his life to the Queen and he means it. "
        "Don't say I didn't warn you."
    )
    dg.add_dialog_node(
        "hint",
        "If you insist on pressing forward... the King values respect above all. "
        "Don't charge in swinging. Let him speak first. It won't save you, "
        "but at least you'll die with your dignity intact. Probably."
    )
    dg.add_dialog_node(
        "about_queen",
        "The Queen? She doesn't even remember your name. You are a card in her "
        "deck, useful until you aren't. She disposed of better players than you."
    )
    dg.add_dialog_node(
        "farewell",
        "Finally. Try not to embarrass yourself too badly out there.",
        node_type="end"
    )

    dg.add_choice("greet",       "menu",        "Fine. I have a few questions.")
    dg.add_choice("greet",       "farewell",    "Never mind. I'm leaving.")

    dg.add_choice("menu",        "about_king",  "Tell me about the King.")
    dg.add_choice("menu",        "hint",        "Any advice for getting past the King?")
    dg.add_choice("menu",        "about_queen", "What is the Queen really like?")
    dg.add_choice("menu",        "farewell",    "I've heard enough. Goodbye.")

    dg.add_choice("about_king",  "menu",        "Anything else I should know?")
    dg.add_choice("about_king",  "farewell",    "Thanks. Goodbye.")
    dg.add_choice("hint",        "menu",        "What else can you tell me?")
    dg.add_choice("hint",        "farewell",    "Understood. Farewell.")
    dg.add_choice("about_queen", "menu",        "Go on, what else?")
    dg.add_choice("about_queen", "farewell",    "Enough. I'm done here.")

    dg.set_start("greet")
    return dg


# ---------------------------------------------------------------------------
# NPC 2 - King of Hearts
# Personality (Lab 1): "Polite, but sure he can defeat you, will protect the
# Queen at all costs." Located at the Poker Table.
# Features: branching (challenge vs. talk), loop (ask more questions).
# ---------------------------------------------------------------------------

def _make_king():
    dg = DialogGraph("King of Hearts")

    dg.add_dialog_node(
        "greet",
        "Good day, traveller. I am the King of Hearts, guardian of this hall. "
        "I hold no ill will toward you, but I cannot allow you to pass. "
        "The Queen's peace must be kept."
    )
    dg.add_dialog_node(
        "challenge",
        "You challenge me? Very well. I respect your courage, even if it borders "
        "on foolishness. Know that I have never lost, and I fight not for glory "
        "but for her. En garde."
    )
    dg.add_dialog_node(
        "ask_queen",
        "The Queen is magnificent. Powerful beyond measure. I have served her "
        "since the first deal was struck at this table. My loyalty is absolute."
    )
    dg.add_dialog_node(
        "ask_past",
        "Before the Queen rose to power, this casino was a place of laughter. "
        "The Joker ruled the table then. But laughter fades, and crowns endure. "
        "That is simply the nature of things."
    )
    dg.add_dialog_node(
        "respect",
        "You show wisdom in holding your tongue. Not many approach me with such "
        "composure. I will give you one chance to turn back, as a courtesy."
    )
    dg.add_dialog_node(
        "farewell",
        "A wise choice. Return when you are prepared. I will be here.",
        node_type="end"
    )

    dg.add_choice("greet",     "challenge", "I challenge you, King.")
    dg.add_choice("greet",     "ask_queen", "Tell me about the Queen.")
    dg.add_choice("greet",     "ask_past",  "What was this place before the Queen?")
    dg.add_choice("greet",     "respect",   "I mean no disrespect, Your Majesty.")

    dg.add_choice("challenge", "farewell",  "Then we shall see.")

    dg.add_choice("ask_queen", "greet",     "I see. I have more questions.")
    dg.add_choice("ask_queen", "farewell",  "Thank you, Your Majesty.")
    dg.add_choice("ask_past",  "greet",     "Interesting. Tell me more.")
    dg.add_choice("ask_past",  "farewell",  "I see. Farewell.")

    dg.add_choice("respect",   "farewell",  "I will return when I am ready.")
    dg.add_choice("respect",   "challenge", "My composure won't stop me. En garde.")

    dg.set_start("greet")
    return dg


# ---------------------------------------------------------------------------
# NPC 3 - Queen of Hearts
# Personality (Lab 1): Greedy, power-mad, sees the Joker as just a buffoon.
# Features: AI node for dynamic taunts, branching end nodes.
# ---------------------------------------------------------------------------

def _make_queen():
    dg = DialogGraph("Queen of Hearts")

    dg.add_dialog_node(
        "entrance",
        "Oh. A buffoon at my door. How quaint. "
        "I suppose even jesters grow bold when they have nothing to lose."
    )
    dg.add_dialog_node(
        "dismiss",
        "You actually think you can challenge ME? I built this table. "
        "I own every card in this deck, including you."
    )
    dg.add_dialog_node(
        "taunt",
        "Go ahead. Ask your little questions. Stall. "
        "The longer you stand here, the more pathetic you look.",
        node_type="fixed"
    )
    dg.add_dialog_node(
        "power",
        "Do you know what it took to sit on this throne? Every deal, every bluff, "
        "every sacrifice. I made them all. And I will not have it taken by "
        "someone who cannot even remember what suit they are."
    )
    dg.add_dialog_node(
        "fury",
        "ENOUGH. Guards! Remove this fool from my sight. Permanently.",
        node_type="end"
    )
    dg.add_dialog_node(
        "cold",
        "You bore me. Leave now, or don't. The outcome is the same for you.",
        node_type="end"
    )

    dg.add_choice("entrance", "dismiss", "I'm here to take your crown.")
    dg.add_choice("entrance", "taunt",   "I just want to talk, Your Majesty.")
    dg.add_choice("entrance", "cold",    "...")

    dg.add_choice("dismiss",  "power",   "You don't own me.")
    dg.add_choice("dismiss",  "fury",    "Then I'll take it by force.")

    dg.add_choice("taunt",    "power",   "What did it cost you to get here?")
    dg.add_choice("taunt",    "fury",    "I've heard enough. Let's end this.")

    dg.add_choice("power",    "fury",    "Then I'll make you remember mine.")

    dg.set_start("entrance")
    return dg


# ---------------------------------------------------------------------------
# NPC_DATA -- the game spawns every entry in this list
# ---------------------------------------------------------------------------

NPC_DATA = [
    {
        "name":        "Jack",
        "grid_x":      5,
        "grid_y":      4,
        "sprite_name": "Jack",
        "dialog":      _make_jack(),
        "ai_handler":  None,
    },
    {
        "name":        "King of Hearts",
        "grid_x":      10,
        "grid_y":      8,
        "sprite_name": "King",
        "dialog":      _make_king(),
        "ai_handler":  None,
    },
    {
        "name":        "Queen of Hearts",
        "grid_x":      20,
        "grid_y":      15,
        "sprite_name": "Queen",
        "dialog":      _make_queen(),
        "ai_handler":  None,
    },
]
