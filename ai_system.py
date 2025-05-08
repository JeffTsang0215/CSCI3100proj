import copy  # Needed for deep copying game state
import itertools
import random
from shared import fps, ai_log

class AISystem:
    def __init__(self, sys):
        self.sys = sys
        self.MaxCombinations = 1000  # Reference to the game system

    def get_card_index_by_name(self, card_list, name):
        for idx, card in enumerate(card_list):
            if card.name == name:
                return idx
        return -1

    def getPlacingIndex(self, card):
        try:
            return self.sys.cardSet["aiHandCard"].index(card)
        except ValueError:
            return -1
    
    
    def calculate_board_score(self):
        A, B, C, D = 1, 1, 1, 1  # Constants for weighting score components
        ai_minion_hp = sum(card.hp for card in self.sys.cardSet["aiCard"])

        player_minion_hp = sum(card.hp for card in self.sys.cardSet["myCard"])

        player_minion_atk = sum(card.atk for card in self.sys.cardSet["myCard"] if card.ext.get("debuff") != ["freeze"])

        ai_minion_atk = sum(card.atk for card in self.sys.cardSet["aiCard"] if card.ext.get("debuff") != ["freeze"])


        ai_cards = len(self.sys.cardSet["aiHandCard"])
        player_cards = len(self.sys.cardSet["myHandCard"])
        
        score = (A * (ai_minion_hp - player_minion_hp) +
                 B * (ai_minion_atk - player_minion_atk) +
                 C * (ai_cards - player_cards) +
                 D * (self.sys.aihp - self.sys.myhp))
        return score

    
    def generate_possible_moves(self):
        moves = []
        available_mana = self.sys.aiMana
        
        # Get all playable cards
        playable_cards = [card for card in self.sys.cardSet["aiHandCard"] if card.cost <= available_mana]

        # Generate all possible card combinations
        all_combos = []
        for r in range(1, len(playable_cards) + 1):  # r = number of cards in the combination
            for combo in itertools.combinations(playable_cards, r):
                if sum(card.cost for card in combo) <= available_mana:  # Only add valid combos
                    all_combos.append(combo)

        # Sort combos to prioritize higher mana usage
        all_combos.sort(key=lambda combo: sum(card.cost for card in combo), reverse=True)

        # Convert each combo into a move set
        for combo in all_combos:
            moves.append(("play_combo", list(combo)))  # Store as a list

        # Consider attacking with minions
        for ai_card in self.sys.cardSet["aiCard"]:
            if not ai_card.attacked:
                for player_card in self.sys.cardSet["myCard"]:
                    if ai_card.atk >= player_card.hp:
                        moves.append(("attack", ai_card.name, player_card.name))
                moves.append(("attack", ai_card.name, "hero"))
                

        return moves

    def execute_best_move(self):
        def move_combo_generator(play_moves, attack_moves, max_combos):
            count = 0
            if play_moves:
                for play_combo in play_moves:
                    for attack_combo in itertools.permutations(attack_moves):
                        used_minions = set()
                        valid_attack_combo = []
                        for attack in attack_combo:
                            if attack[1] not in used_minions:
                                valid_attack_combo.append(attack)
                                used_minions.add(attack[1])
                        for i in range(len(valid_attack_combo) + 1):
                            yield list(valid_attack_combo[:i]) + [play_combo] + list(valid_attack_combo[i:])
                            count += 1
                            if count >= max_combos:
                                return
            else:
                for attack_combo in itertools.permutations(attack_moves):
                    used_minions = set()
                    valid_attack_combo = []
                    for attack in attack_combo:
                        if attack[1] not in used_minions:
                            valid_attack_combo.append(attack)
                            used_minions.add(attack[1])
                    yield valid_attack_combo
                    count += 1
                    if count >= max_combos:
                        return

        # Store initial game state
        original_state = copy.deepcopy(self.sys.cardSet)
        original_mana = self.sys.aiMana
        original_ai_hp = self.sys.aihp
        original_player_hp = self.sys.myhp
        original_aiCardOrder = self.sys.aiCardOrder.copy()

        best_score = self.calculate_board_score()
        best_move_sequence = None

        play_moves = []
        attack_moves = []
        
        possible_moves = self.generate_possible_moves()

        for move in possible_moves:
            if move[0] == "play_combo":
                play_moves.append(move)
            elif move[0] == "attack":
                attack_moves.append(move)

        play_moves.sort(key=lambda m: sum(card.cost for card in m[1]), reverse=True)

        # Generate move combinations using a capped generator
        move_combinations = list(move_combo_generator(play_moves, attack_moves, self.MaxCombinations))
        #print("The number of move combinations: " + str(len(move_combinations)))

        #Emergency moves for decoration
        if len(move_combinations) >= self.MaxCombinations:
            print("Too many move combinations or none found. Entering emergency mode.")
            emergency_moves = [("attack", ai_card.name, "hero") for ai_card in self.sys.cardSet["aiCard"]]
            if play_moves:
                highest_mana_play = max(play_moves, key=lambda m: sum(card.cost for card in m[1]))
                emergency_moves.append(highest_mana_play)
            move_combinations = [emergency_moves]
            best_move_sequence = emergency_moves #for safety

        random.shuffle(move_combinations)

        for move_sequence in move_combinations:
            self.sys.cardSet = copy.deepcopy(original_state)
            self.sys.aiMana = original_mana
            self.sys.aihp = original_ai_hp
            self.sys.myhp = original_player_hp
            self.sys.aiCardOrder = original_aiCardOrder.copy()

            skip_sequence = False  # Flag to indicate if the current move_sequence should be skipped

            for move in move_sequence:
                if skip_sequence:
                    break  # Exit the inner loop if the sequence is invalid

                if move[0] == "play_combo":
                    for card in move[1]:
                        if self.sys.aiMana >= card.cost:
                            placing_index = self.getPlacingIndex(card)
                            if(self.sys.cardSet["aiHandCard"][placing_index].ext["type"] == "minion" and len(self.sys.cardSet["aiCard"]) < 7 ):
                                self.sys.placeCardTo(placing_index, len(self.sys.cardSet["myCard"]))
                            else:
                                # spell card
                                if("skill" in self.sys.cardSet["aiHandCard"][placing_index].ext):
                                    if("freeze" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        target = range(len(self.sys.cardSet["myCard"]))
                                        if(len(self.sys.cardSet["myCard"]) > self.sys.cardSet["aiHandCard"][placing_index].ext["n"]):
                                            target = random.sample(range(len(self.sys.cardSet["myCard"])), self.sys.cardSet["aiHandCard"][placing_index].ext["n"])
                                        for j in target:
                                            self.sys.freeze(self.sys.cardSet["myCard"][j])
                                    if ("fullAtk" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        self.sys.fullAtk(False, self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                    if ("draw" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        for j in range(self.sys.cardSet["aiHandCard"][placing_index].ext["n"]):
                                            self.sys.giveCard(True)
                                    if ("cure" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"] and len(self.sys.cardSet["aiCard"]) > 0):
                                        if(self.sys.cardSet["aiHandCard"][placing_index].ext["random"]):
                                            target = random.sample(range(len(self.sys.cardSet["aiCard"])), 1)
                                            self.sys.cure(self.sys.cardSet["aiCard"][target[0]], self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                        else:
                                            target = 0
                                            self.sys.cure(self.sys.cardSet["aiHandCard"][target], self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                self.sys.aiMana -= self.sys.cardSet["aiHandCard"][placing_index].cost
                                self.sys.rubbishBin = self.sys.cardSet["aiHandCard"].pop(placing_index)

                elif move[0] == "attack":
                    ai_index = self.get_card_index_by_name(self.sys.cardSet["aiCard"], move[1])
                    if ai_index == -1:
                        print(f"❌ AI card '{move[1]}' not found.")
                        skip_sequence = True  # Mark sequence as invalid
                        continue  # Skip to next move, but the flag will cause a break

                    if move[2] == "hero":
                        target_index = 99
                    else:
                        target_index = self.get_card_index_by_name(self.sys.cardSet["myCard"], move[2])
                        if target_index == -1:
                            print(f"❌ Player card '{move[2]}' not found.")
                            skip_sequence = True  # Mark sequence as invalid
                            continue  # Skip to next move, but the flag will cause a break

                    if not self.sys.cardSet["aiCard"][ai_index].attacked:
                        self.sys.attack(ai_index, target_index, False)

            if skip_sequence:
                continue  # Skip to the next move_sequence in move_combinations

            self.sys.checkAliveAI()

            if len(self.sys.cardSet["aiCard"]) > 7:
                new_score = -9999
            else:
                new_score = self.calculate_board_score()

            if self.sys.myhp <= 0:
                new_score = 9999
            else:
                new_score = self.calculate_board_score()

            if new_score > best_score:
                best_score = new_score
                best_move_sequence = move_sequence

        # Final execution of best sequence
        self.sys.cardSet = copy.deepcopy(original_state)
        self.sys.aiMana = original_mana
        self.sys.aihp = original_ai_hp
        self.sys.myhp = original_player_hp
        self.sys.aiCardOrder = original_aiCardOrder.copy()

        # # Generate n empty move between each
        # n = int(fps*0.5)
        # best_move_sequence_wait = []
        # for event in best_move_sequence:
        #     for i in range(n):
        #         best_move_sequence_wait.append(("wait",1))
        #     best_move_sequence_wait.append(event)
        # for i in range(n):
        #         best_move_sequence_wait.append(("wait",1))

        if best_move_sequence:
            print(f"Best move sequence selected: {best_move_sequence}")
            for move in best_move_sequence:
                if(len(ai_log) < 6):
                    ai_log.append(move)
                else:
                    ai_log.pop(0)
                    ai_log.append(move)
                if move[0] == "play_combo":
                    for card in move[1]:
                        if self.sys.aiMana >= card.cost:
                            placing_index = self.getPlacingIndex(card)
                            if(self.sys.cardSet["aiHandCard"][placing_index].ext["type"] == "minion" and len(self.sys.cardSet["aiCard"]) < 7 ):
                                self.sys.placeCardTo(placing_index, len(self.sys.cardSet["myCard"]))
                            else:
                                # spell card
                                if("skill" in self.sys.cardSet["aiHandCard"][placing_index].ext):
                                    if("freeze" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        target = range(len(self.sys.cardSet["myCard"]))
                                        if(len(self.sys.cardSet["myCard"]) > self.sys.cardSet["aiHandCard"][placing_index].ext["n"]):
                                            target = random.sample(range(len(self.sys.cardSet["myCard"])), self.sys.cardSet["aiHandCard"][placing_index].ext["n"])
                                        for j in target:
                                            self.sys.freeze(self.sys.cardSet["myCard"][j])
                                    if ("fullAtk" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        self.sys.fullAtk(False, self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                    if ("draw" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"]):
                                        for j in range(self.sys.cardSet["aiHandCard"][placing_index].ext["n"]):
                                            self.sys.giveCard(True)
                                    if ("cure" in self.sys.cardSet["aiHandCard"][placing_index].ext["skill"] and len(self.sys.cardSet["aiCard"]) > 0):
                                        if(self.sys.cardSet["aiHandCard"][placing_index].ext["random"]):
                                            target = random.sample(range(len(self.sys.cardSet["aiCard"])), 1)
                                            self.sys.cure(self.sys.cardSet["aiCard"][target[0]], self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                        else:
                                            target = 0
                                            self.sys.cure(self.sys.cardSet["aiHandCard"][target], self.sys.cardSet["aiHandCard"][placing_index].ext["atk"])
                                self.sys.aiMana -= self.sys.cardSet["aiHandCard"][placing_index].cost
                                self.sys.rubbishBin = self.sys.cardSet["aiHandCard"].pop(placing_index)
                elif move[0] == "attack":
                    ai_index = self.get_card_index_by_name(self.sys.cardSet["aiCard"], move[1])
                    if ai_index == -1:
                        print(f"❌ AI card '{move[1]}' not found.")
                        continue

                    if move[2] == "hero":
                        target_index = 99
                    else:
                        target_index = self.get_card_index_by_name(self.sys.cardSet["myCard"], move[2])
                        if target_index == -1:
                            print(f"❌ Player card '{move[2]}' not found.")
                            continue

                    if not self.sys.cardSet["aiCard"][ai_index].attacked:
                        self.sys.attack(ai_index, target_index, False)

        self.sys.checkAlive()


