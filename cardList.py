import shared
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
scale1 = shared.WIDTH / 1080

# COMMON CARDS
card.append([0, 1, 3, "Goblin Scout", "common", scale1, "description", "Bob the undying.png", {"type": "minion"}])
card.append([1, 2, 4, "Elven Archer", "common", scale1, "description", "ninja.png", {"type": "minion"}])
card.append([1, 1, 5, "Skeletal Minion", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([1, 1, 6, "Frost Mage", "common", scale1, "description", "cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([1, 2, 3, "Forest Dryad", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 3, 6, "Arcane Apprentice", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 2, 3, "Ice Elemental", "common", scale1, "description", "cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([2, 4, 5, "Troll Warrior", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])

# RARE CARDS
card.append([2, 5, 3, "Assassin", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 3, 7, "Battle Medic", "rare", scale1, "description", "cardTemp.png", {"type": "minion", "skill": "cure", "n": 3}])
card.append([3, 3, 6, "Paladin Guardian", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 4, 5, "Orc Berserker", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 5, 6, "Jungle Panther", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 8, "Flamecaller", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 3, 9, "Spirit Guardian", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 7, "Fireborn Champion", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])

# EPIC CARDS
card.append([3, 4, 7, "Vampire Lord", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 5, 5, "Berserker Chief", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 5, 6, "Dragon Hatchling", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "Dark Knight", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 8, "Desert King", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Elder Sage", "epic", scale1, "description", "cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
#card.append([3, 0, 0, "Blizzard", "epic", scale1, "description", "cardTemp.png", {"type": "spell", "skill": "freeze", "n": 2}])
#card.append([4, 0, 0, "Firestorm", "epic", scale1, "description", "cardTemp.png", {"type": "spell", "skill": "fullAtk"}])

# LEGENDARY CARDS
card.append([4, 5, 8, "Infernal Demon", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Ancient Wizard", "legendary", scale1, "description", "cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
card.append([5, 5, 10, "Storm Titan", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Titan Guardian", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Elder Dragon", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 5, 9, "Fire Golem", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "Mystic Phoenix", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 9, "Void Lord", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
