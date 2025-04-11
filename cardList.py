import shared
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

# card.append([cost, atk, hp, name, rarity, scale factor, description, image, ext])
card = []
scale1 = shared.WIDTH / 1080

# COMMON CARDS
card.append([0, 1, 3, "Goblin", "common", scale1, "description", "Bob the undying.png", {"type": "minion"}])
card.append([1, 2, 4, "Archer", "common", scale1, "description", "ninja.png", {"type": "minion"}])
card.append([1, 1, 5, "SkeletalMinion", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([1, 1, 6, "Frost", "common", scale1, "freeze 1 enemy", "cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([1, 2, 3, "ForestDryad", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 3, 6, "Arcane", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 2, 3, "Ice", "common", scale1, "freeze 1 enemy", "cardTemp.png", {"type": "minion", "skill": "freeze", "n": 1}])
card.append([2, 4, 5, "Warrior", "common", scale1, "description", "cardTemp.png", {"type": "minion"}])

# RARE CARDS
card.append([2, 5, 3, "Assassin", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([2, 0, 0, "Medic", "rare", scale1, "ramdomly cure one card by 3 hp", "cardTemp.png", {"type": "spell", "skill": "cure", "atk": 3, "random": True}])
card.append([3, 3, 6, "Paladin", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 4, 5, "Berserker", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 5, 6, "Panther", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 8, "Flamecaller", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 3, 9, "Guardian", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 7, "Champion", "rare", scale1, "description", "cardTemp.png", {"type": "minion"}])

# EPIC CARDS
card.append([3, 4, 7, "Vampire", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([3, 5, 5, "Berserker", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 5, 6, "Dragon", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "DarkKnight", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 8, "DesertKing", "epic", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "ElderSage", "epic", scale1, "draw 2 cards", "cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
card.append([3, 0, 0, "Blizzard", "epic", scale1, "freeze 2 enemies", "cardTemp.png", {"type": "spell", "skill": "freeze", "n": 2}])
card.append([4, 0, 0, "Firestorm", "epic", scale1, "deal 2 damage to all enemy", "cardTemp.png", {"type": "spell", "skill": "fullAtk", "atk": 2}])

# LEGENDARY CARDS
card.append([4, 5, 8, "Infernal", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Wizard", "legendary", scale1, "draw 2 cards", "cardTemp.png", {"type": "minion", "skill": "draw", "n": 2}])
card.append([5, 5, 10, "StormTitan", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "Titan", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 10, "ElderDragon", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 5, 9, "FireGolem", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([4, 4, 9, "Phoenix", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
card.append([5, 5, 9, "Void", "legendary", scale1, "description", "cardTemp.png", {"type": "minion"}])
