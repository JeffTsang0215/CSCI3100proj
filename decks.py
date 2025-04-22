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
            "Goblin", "Goblin",
            "Archer", "Archer",
            "SkeletalMinion", "SkeletalMinion",
            "Frost", "Frost",
            "Forest Guide", "Forest Guide",
            "Body Bagger", "Body Bagger",
            "Ice", "Ice",
            "Air guitarlist", "Air guitarlist",
            "Abusive Sergeant", "Abusive Sergeant",
            "Fire Fly", "Fire Fly",
            "Blazing Battlemage", "Blazing Battlemage",
            "Medic", "Medic",
            "Elven Archer", "Elven Archer",
            "Dancing Swords", "Dancing Swords",
            "Devilsaur Egg", "Devilsaur Egg",
        ]
    }
]

#AI deck 1
AI_deck_1 = [
    {
        "name": "Creeper Core",
        "cards": [
            "Penguin", "Penguin",
            "Goblin", "Goblin",
            "Tar Creeper", "Tar Creeper",
            "Fen Creeper", "Fen Creeper",
            "Bog Creeper", "Bog Creeper",
            "Frost", "Frost",
            "Ice", "Ice",
            "Blizzard", "Blizzard",
            "Firestorm", "Firestorm",
            "Medic", "Medic",
            "Treasure Chest", "Treasure Chest",
            "Gatekeeper", "Gatekeeper",
            "Cobalt Scalebane", "Cobalt Scalebane",
            "Forest Guide", "Forest Guide",
            "DarkKnight", "DarkKnight",
        ]
    }
]

#AI_deck_2
AI_deck_2 = [
    {
        "name": "Aggro Squad",
        "cards": [
            "Archer", "Archer",
            "SkeletalMinion", "SkeletalMinion",
            "Air guitarlist", "Air guitarlist",
            "Battlemage", "Battlemage",
            "Elven Archer", "Elven Archer",
            "Vampire", "Vampire",
            "Scaleworm", "Scaleworm",
            "Dragonslayer", "Dragonslayer",
            "Devilsaur Egg", "Devilsaur Egg",
            "Fire Fly", "Fire Fly",
            "Sergeant", "Sergeant",
            "Dancing Swords", "Dancing Swords",
            "Dr. Boom", "Dr. Boom",
            "StormTitan", "StormTitan",
            "Phoenix", "Phoenix"
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