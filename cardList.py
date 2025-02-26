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

# card.append([cost, atk, hp, name, rarity, scale factor, image, ext])
card = []

# COMMON CARDS
card.append([0, 1, 3, "Goblin Scout", "common", "description", 1, None, {"type": "minion"}])
card.append([1, 2, 4, "Elven Archer", "common", "description", 1, None, {"type": "minion"}])
card.append([1, 1, 5, "Skeletal Minion", "common", "description", 1, None, {"type": "minion"}])
card.append([1, 1, 6, "Frost Mage", "common", "description", 1, None, {"type": "minion", "skill": "freeze", "n": 1}])
card.append([1, 2, 3, "Forest Dryad", "common", "description", 1, None, {"type": "minion"}])
card.append([2, 3, 6, "Arcane Apprentice", "common", "description", 1, None, {"type": "minion"}])
card.append([2, 2, 3, "Ice Elemental", "common", "description", 1, None, {"type": "minion", "skill": "freeze", "n": 1}])
card.append([2, 4, 5, "Troll Warrior", "common", "description", 1, None, {"type": "minion"}])
card.append([3, 4, 6, "Swamp Guardian", "common", "description", 1, None, {"type": "minion"}])
card.append([3, 3, 7, "Stone Guardian", "common", "description", 1, None, {"type": "minion"}])

# RARE CARDS
card.append([2, 5, 3, "Assassin", "rare", "description", 1, None, {"type": "minion"}])
card.append([2, 3, 7, "Battle Medic", "rare", "description", 1, None, {"type": "minion", "skill": "cure", "n": 3}])
card.append([3, 3, 6, "Paladin Guardian", "rare", "description", 1, None, {"type": "minion"}])
card.append([3, 4, 5, "Orc Berserker", "rare", "description", 1, None, {"type": "minion"}])
card.append([3, 5, 6, "Jungle Panther", "rare", "description", 1, None, {"type": "minion"}])
card.append([4, 4, 8, "Flamecaller", "rare", "description", 1, None, {"type": "minion"}])
card.append([4, 3, 9, "Spirit Guardian", "rare", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 7, "Fireborn Champion", "rare", "description", 1, None, {"type": "minion"}])
card.append([2, 0, 0, "Arcane Blast", "rare", "description", 1, None, {"type": "spell", "skill": "fullAtk"}])
card.append([3, 0, 0, "Healing Rain", "rare", "description", 1, None, {"type": "spell", "skill": "cure", "n": 5}])

# EPIC CARDS
card.append([3, 4, 7, "Vampire Lord", "epic", "description", 1, None, {"type": "minion"}])
card.append([3, 5, 5, "Berserker Chief", "epic", "description", 1, None, {"type": "minion"}])
card.append([4, 5, 6, "Dragon Hatchling", "epic", "description", 1, None, {"type": "minion"}])
card.append([4, 4, 9, "Dark Knight", "epic", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 8, "Desert King", "epic", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 10, "Elder Sage", "epic", "description", 1, None, {"type": "minion", "skill": "draw", "n": 2}])
card.append([3, 0, 0, "Blizzard", "epic", "description", 1, None, {"type": "spell", "skill": "freeze", "n": 2}])
card.append([4, 0, 0, "Firestorm", "epic", "description", 1, None, {"type": "spell", "skill": "fullAtk"}])
card.append([5, 0, 0, "Mass Resurrect", "epic", "description", 1, None, {"type": "spell", "skill": "summon", "n": 4}])

# LEGENDARY CARDS
card.append([4, 5, 8, "Infernal Demon", "legendary", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 10, "Ancient Wizard", "legendary", "description", 1, None, {"type": "minion", "skill": "draw", "n": 2}])
card.append([5, 5, 10, "Storm Titan", "legendary", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 10, "Titan Guardian", "legendary", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 10, "Elder Dragon", "legendary", "description", 1, None, {"type": "minion"}])
card.append([4, 5, 9, "Fire Golem", "legendary", "description", 1, None, {"type": "minion"}])
card.append([4, 4, 9, "Mystic Phoenix", "legendary", "description", 1, None, {"type": "minion"}])
card.append([5, 5, 9, "Void Lord", "legendary", "description", 1, None, {"type": "minion"}])
card.append([4, 0, 0, "Divine Protection", "legendary", "description", 1, None, {"type": "spell"}])
card.append([5, 0, 0, "Time Warp", "legendary", "description", 1, None, {"type": "spell"}])
