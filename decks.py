import shared
import json
import sqlite3
import os

# Database setup
conn = sqlite3.connect(shared.path + 'database/database.db')
cursor = conn.cursor()

# starter deck data
starter_deck = [
    {
        "name": "Starter Deck",
        "cards": [
            "Goblin",
            "Goblin",
            "Goblin",
            "Archer",
            "Archer",
            "Archer",
            "SkeletalMinion",
            "SkeletalMinion",
            "Frost",
            "Frost",
            "ForestDryad",
            "ForestDryad",
            "Arcane",
            "Arcane",
            "Assassin",
            "Assassin",
            "Medic",
            "Medic",
            "Paladin",
            "Paladin",
            "Berserker",
            "Berserker",
            "Panther",
            "FlameCaller",
            "FrenziedBerserker",
            "FrenziedBerserker",
            "Blizzard",
            "Blizzard",
            "Firestorm",
            "Firestorm"
        ]
    }
]

starter_deck_json = json.dumps(starter_deck)

# Default deck data
decks = []

# load decks from database
def load_decks():
    global decks
    cursor.execute("SELECT decks FROM user_card_collection WHERE username = ?", (shared.user_name,))
    decks_data = cursor.fetchone()
    decks = json.loads(decks_data[0])

# Save function to update file when decks change
def save_decks():
    cursor.execute("UPDATE user_card_collection SET decks = ? WHERE username = ?", (json.dumps(decks), shared.user_name))
    conn.commit()