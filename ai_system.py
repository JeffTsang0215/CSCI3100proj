import copy  # Needed for deep copying game state
import itertools
import random

class AISystem:
    def __init__(self, sys):
        self.sys = sys
        self.MaxCombinations = 10000  # Reference to the game system

    def getPlacingIndex(self, card):
        """Find the index of a card in aiHandCard based on cost, attack, and HP."""
        for i, hand_card in enumerate(self.sys.cardSet["aiHandCard"]):
            if hand_card.cost == card.cost and hand_card.atk == card.atk and hand_card.hp == card.hp:
                return i  # Return the index if found
        return -1  # Return -1 if card is not found
    
    
    def calculate_board_score(self):
        A, B, C, D = 1, 1, 1, 1  # Constants for weighting score components
        ai_minion_hp = sum(card.hp for card in self.sys.cardSet["aiCard"])

        player_minion_hp = sum(card.hp for card in self.sys.cardSet["myCard"])

        ai_minion_atk = sum(card.atk for card in self.sys.cardSet["aiCard"])

        player_minion_atk = sum(card.atk for card in self.sys.cardSet["myCard"])

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
        for i, ai_card in enumerate(self.sys.cardSet["aiCard"]):
            if not ai_card.attacked:  # Can attack
                # Attack player minions first
                for j, player_card in enumerate(self.sys.cardSet["myCard"]):
                    if ai_card.atk >= player_card.hp:  # Ensure good trade
                        moves.append(("attack", i, j))
                # Attack player hero
                moves.append(("attack", i, 99))
        

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

        #Emergency moves for decoration
        if not move_combinations:
            print("Too many move combinations or none found. Entering emergency mode.")
            emergency_moves = [("attack", i, 99) for i in range(len(self.sys.cardSet["aiCard"]))]
            if play_moves:
                highest_mana_play = max(play_moves, key=lambda m: sum(card.cost for card in m[1]))
                emergency_moves.append(highest_mana_play)
            move_combinations = [emergency_moves]

        random.shuffle(move_combinations)

        for move_sequence in move_combinations:
            self.sys.cardSet = copy.deepcopy(original_state)
            self.sys.aiMana = original_mana
            self.sys.aihp = original_ai_hp
            self.sys.myhp = original_player_hp

            for move in move_sequence:
                if move[0] == "play_combo":
                    for card in move[1]:
                        if self.sys.aiMana >= card.cost:
                            placing_index = self.getPlacingIndex(card)
                            self.sys.placeCardTo(placing_index, len(self.sys.cardSet["aiCard"]))
                elif move[0] == "attack":
                    if not self.sys.cardSet["aiCard"][move[1]].attacked:
                        self.sys.attack(move[1], move[2], False)

            self.sys.checkAlive()

            if len(self.sys.cardSet["aiCard"]) > 7:
                new_score = -9999
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

        if best_move_sequence:
            print(f"Best move sequence selected: {best_move_sequence}")
            for move in best_move_sequence:
                if move[0] == "play_combo":
                    for card in move[1]:
                        if self.sys.aiMana >= card.cost:
                            placing_index = self.getPlacingIndex(card)
                            self.sys.placeCardTo(placing_index, len(self.sys.cardSet["aiCard"]))
                elif move[0] == "attack":
                    if not self.sys.cardSet["aiCard"][move[1]].attacked:
                        self.sys.attack(move[1], move[2], False)

        self.sys.checkAlive()
        self.sys.switchTurn()

