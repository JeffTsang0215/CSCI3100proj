import shared
import sqlite3
import json
#ext:
#  type:
#    minion
#    spell
#  skill:
#    fullAtk
#    freeze n
#    draw n
#    cure n random
#  n: int
#  random: bool
#  atk: int
#  debuff: [string]list

# Database setup
conn = sqlite3.connect(shared.path + 'database/database.db')
cursor = conn.cursor()

# card.append([cost, atk, hp, name, rarity, scale factor,descrption , image, ext])

scale1 = shared.WIDTH / 1080
card_dict = {}
card = []

# COMMON CARDS (100 gold)
card_dict[1] = [0, 1, 1, "Goblin", "common", scale1, "", "Bob the undying.png", {"type": "minion"}] #1
card_dict[2] = [1, 2, 1, "Archer", "common", scale1, "", "ninja.png", {"type": "minion"}]
card_dict[3] = [1, 1, 3, "SkeletalMinion", "common", scale1, "", "Skeletal_Sidekick.png", {"type": "minion"}]
card_dict[4] = [1, 1, 2, "Frost", "common", scale1, "freeze 1 enemy", "Ymirjar_Frostbreaker.png", {"type": "minion", "skill": "freeze", "n": 1}]
card_dict[5] = [1, 1, 3, "Forest Guide", "common", scale1, "", "Forest_Guide_full.png", {"type": "minion"}]
card_dict[6] = [2, 2, 3, "Body Bagger", "common", scale1, "", "Body_Bagger_full.png", {"type": "minion"}]
card_dict[7] = [2, 2, 2, "Ice", "common", scale1, "freeze 1 enemy", "Ice_Rager_full.png", {"type": "minion", "skill": "freeze", "n": 1}]
card_dict[8] = [2, 2, 3, "Air guitarlist", "common", scale1, "", "air_guitarlist.png", {"type": "minion"}]

#new common cards
card_dict[33] = [6, 6, 6, "Abusive Sergeant", "common", scale1, "", "Abusive_Sergeant.png", {"type": "minion"}]
card_dict[34] = [6, 5, 7, "Fire Fly", "common", scale1, "", "Fire_Fly_full.png", {"type": "minion"}]
card_dict[35] = [0, 1, 1, "Snowflipper Penguin", "common", scale1, "", "Snowflipper_Penguin_full.png", {"type": "minion"}]
card_dict[36] = [3, 3, 5, "Tar Creeper", "common", scale1, "", "Tar_Creeper_full.png", {"type": "minion"}]
card_dict[37] = [4, 3, 3, "Arena Treasure Chest", "common", scale1, "Draw 2 cards", "Arena_Treasure_Chest_full.png", {"type": "minion", "skill": "draw", "n": 2}]

# RARE CARDS (500 gold)
card_dict[9] = [2, 3, 2, "Blazing Battlemage", "rare", scale1, "", "Blazing_Battlemage_full.png", {"type": "minion"}] #9
card_dict[10] = [2, 0, 0, "Medic", "rare", scale1, "Ramdomly cure \n 1 CARD by \n 3 hp", "Forbidden_Healing_full.png", {"type": "spell", "skill": "cure", "atk": 3, "random": True}]
card_dict[11] = [3, 3, 4, "Elven Archer", "rare", scale1, "test", "Elven_Archer.png", {"type": "minion"}]
card_dict[12] = [4, 4, 5, "Dancing Swords", "rare", scale1, "", "Dancing_Swords_full.png", {"type": "minion"}]
card_dict[13] = [3, 5, 2, "Devilsaur Egg", "rare", scale1, "", "Devilsaur Egg.png", {"type": "minion"}]
card_dict[14] = [4, 3, 6, "Dragonslayer", "rare", scale1, "", "Dragonslayer_full.png", {"type": "minion"}]
card_dict[15] = [4, 2, 7, "Forest Guide", "rare", scale1, "", "Forest_Guide_full.png", {"type": "minion"}]
card_dict[16] = [5, 5, 6, "Champion", "rare", scale1, "", "Lone_Champion_full.png", {"type": "minion"}]

# EPIC CARDS (1000 gold)
card_dict[17] = [3, 4, 3, "Vampire", "epic", scale1, "", "Blood_of_huun_full.png", {"type": "minion"}] #17
card_dict[18] = [3, 1, 8, "Scaleworm", "epic", scale1, "", "Scaleworm_full.png", {"type": "minion"}]
card_dict[19] = [4, 2, 6, "Cobalt Scalebane", "epic", scale1, "", "Cobalt_Scalebane_full.png", {"type": "minion"}]
card_dict[20] = [4, 4, 5, "DarkKnight", "epic", scale1, "", "The_Black_Knight_full.png", {"type": "minion"}]
card_dict[21] = [5, 5, 6, "Rotten Applebaum", "epic", scale1, "", "Rotten_Applebaum_full.png", {"type": "minion"}]
card_dict[22] = [5, 5, 5, "Tormented Dreadwing", "epic", scale1, "Draw 2 cards", "Tormented_Dreadwing_full.png", {"type": "minion", "skill": "draw", "n": 2}]
card_dict[23] = [3, 0, 0, "Blizzard", "epic", scale1, "Freeze 2 enemies", "Blizzard_full.png", {"type": "spell", "skill": "freeze", "n": 2}]
card_dict[24] = [4, 0, 0, "Firestorm", "epic", scale1, "Deal 2 damage \n to all enemy", "Wildfire_full.png", {"type": "spell", "skill": "fullAtk", "atk": 2}]

# LEGENDARY CARDS (5000 gold)
card_dict[25] = [10, 12, 12, "Deathwing the Destroyer", "legendary", scale1, "", "Deathwing_the_Destroyer_full.png", {"type": "minion"}] #25
card_dict[26] = [5, 5, 6, "Dr. Boom", "legendary", scale1, "draw 2 cards", "Dr._Boom_full.png", {"type": "minion", "skill": "draw", "n": 2}]
card_dict[27] = [5, 8, 8, "StormTitan", "legendary", scale1, "", "Amitus,_the_Peacekeeper_full.png", {"type": "minion"}]
card_dict[28] = [9, 6, 12, "Sargeras, the Destroyer", "legendary", scale1, "", "Sargeras,_the_Destroyer_full.png", {"type": "minion"}]
card_dict[29] = [5, 3, 10, "ElderDragon", "legendary", scale1, "", "Temporus_full.png", {"type": "minion"}]
card_dict[30] = [4, 5, 8, "FireGolem", "legendary", scale1, "", "Saruun_full.png", {"type": "minion"}]
card_dict[31] = [4, 7, 5, "Phoenix", "legendary", scale1, "", "Pyros_full.png", {"type": "minion"}]
card_dict[32] = [5, 7, 9, "Gaia, the Techtonic", "legendary", scale1, "", "Gaia,_the_Techtonic_full.png", {"type": "minion"}]


# default cards that are unlocked for each new user
starter_card = [
    # Common cards
    1,  # Goblin
    2,  # Archer
    3,  # SkeletalMinion
    4,  # Frost
    5,  # Forest Guide
    6,  # Body Bagger
    7,  # Ice
    8,  # Air guitarlist
    33, # Abusive Sergeant
    34, # Fire Fly

    # Rare cards
    9,  # Blazing Battlemage
    10, # Medic
    11, # Elven Archer
    12, # Dancing Swords
    13, # Devilsaur Egg
    14, # Dragonslayer
    15, # Forest Guide
    16, # Champion

    # Epic cards
    17, # Vampire
    18, # FrenziedBerserker
    19, # Dragon
    20, # DarkKnight
    21, # DesertKing
    22, # ElderSage
    23, # Blizzard
    24, # Firestorm

    # Legendary cards
    25, # Infernal
    26, # Wizard
    27, # StormTitan
    28, # Titan
    29, # ElderDragon
    30, # FireGolem
    31, # Phoenix
    32, # Void

    #New common cards
    33,34,35,36,37
    
]


# store start cards in database with json format
starter_card_json = json.dumps(starter_card)

def load_cards_from_json(cards_json: str):  # input should be (unlock_cards_data[0])
    card_id_list = json.loads(cards_json)
    card = [] # return this card set at the end
    for card_id in card_id_list:
        card.append(card_dict[card_id])
    return card

def load_unlock_cards():
    global card
    cursor.execute("SELECT unlock_cards FROM user_card_collection WHERE username = ?", (shared.user_name,))
    unlock_cards_data = cursor.fetchone()
    card = load_cards_from_json(unlock_cards_data[0])