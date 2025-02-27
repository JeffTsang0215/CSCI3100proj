#ext:
#  type:
#    minion
#    spell
#  skill:
#    summon n
#    fullAtk
#    freeze n
#    draw n
#    cure n 
#  n: int
#  atk: int

# card.append([cost, atk, hp, name, rarity, scale factor, description, image, ext])
card = []

# COMMON CARDS
card.append([0, 1, 3, "Goblin Scout", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([1, 2, 4, "Elven Archer", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([1, 1, 5, "Skeletal Minion", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([1, 1, 6, "Frost Mage", "common", 1, "description", "image/cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([1, 2, 3, "Forest Dryad", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([2, 3, 6, "Arcane Apprentice", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([2, 2, 3, "Ice Elemental", "common", 1, "description", "image/cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([2, 4, 5, "Troll Warrior", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
#card.append([3, 4, 6, "Swamp Guardian", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])
#card.append([3, 3, 7, "Stone Guardian", "common", 1, "description", "image/cardTemp.png", {"type": "minion"}])

# RARE CARDS
card.append([2, 5, 3, "Assassin", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([2, 3, 7, "Battle Medic", "rare", 1, "description", "image/cardTemp.png", {"type": "minion", "skill": "cure", "n": 3}])
card.append([3, 3, 6, "Paladin Guardian", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([3, 4, 5, "Orc Berserker", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([3, 5, 6, "Jungle Panther", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 4, 8, "Flamecaller", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 3, 9, "Spirit Guardian", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 7, "Fireborn Champion", "rare", 1, "description", "image/cardTemp.png", {"type": "minion"}])
#card.append([2, 0, 0, "Arcane Blast", "rare", 1, "description", "image/cardTemp.png", {"type": "spell", "skill": "fullAtk"}])
#card.append([3, 0, 0, "Healing Rain", "rare", 1, "description", "image/cardTemp.png", {"type": "spell", "skill": "cure", "n": 5}])

# EPIC CARDS
card.append([3, 4, 7, "Vampire Lord", "epic", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([3, 5, 5, "Berserker Chief", "epic", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 5, 6, "Dragon Hatchling", "epic", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "Dark Knight", "epic", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 8, "Desert King", "epic", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Elder Sage", "epic", 1, "description", "image/cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
card.append([3, 0, 0, "Blizzard", "epic", 1, "description", "image/cardTemp.png", {"type": "spell", "skill": "freeze", "n": 2}])
card.append([4, 0, 0, "Firestorm", "epic", 1, "description", "image/cardTemp.png", {"type": "spell", "skill": "fullAtk"}])
#card.append([5, 0, 0, "Mass Resurrect", "epic", 1, "description", "image/cardTemp.png", {"type": "spell", "skill": "summon", "n": 4}])

# LEGENDARY CARDS
card.append([4, 5, 8, "Infernal Demon", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Ancient Wizard", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
card.append([5, 5, 10, "Storm Titan", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Titan Guardian", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Elder Dragon", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 5, 9, "Fire Golem", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "Mystic Phoenix", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
card.append([5, 5, 9, "Void Lord", "legendary", 1, "description", "image/cardTemp.png", {"type": "minion"}])
#card.append([4, 0, 0, "Divine Protection", "legendary", 1, "description", "image/cardTemp.png", {"type": "spell"}])
