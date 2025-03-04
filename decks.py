import shared
import json
import os

# File path for storing deck data
DECKS_FILE = "decks.json"

# Default deck data
decks = []

# Load decks from file
if os.path.exists(DECKS_FILE):
    with open(DECKS_FILE, "r") as f:
        try:
            decks = json.load(f)
        except json.JSONDecodeError:
            decks = []  # Reset if file is corrupted
else:
    decks = []  # Initialize empty if no file exists

# Save function to update file when decks change
def save_decks():
    with open(DECKS_FILE, "w") as f:
        json.dump(decks, f, indent=4)
