import random

from RiskGame.Mechanics import attack, fortify
from RiskGame.Mechanics import determine_dice_count
from RiskGame.Card import Card
from RiskGame.RiskBoard import Board


board = Board()
class Player:

    total_sets_traded = 0

    def __init__(self, name):
        self.name = name
        self.territories = []
        self.armies = 0  # This can be adjusted based on the initial game setup
        self.cards = []
        self.conquered_territory = False

    @property
    def is_active(self):
        """Check if the player is still active (controls at least one territory)."""
        return len(self.territories) > 0

    # Temporary method to add test cards
    def add_test_cards(self):
        # Adding a set of tradeable cards
        self.cards.extend([Card("Infantry"), Card("Infantry"), Card("Infantry")])
        print(f"{self.name} received test cards: {[card.type for card in self.cards]}")



    def add_territory(self, territory):
        """ Adds a territory to the player's control """
        self.territories.append(territory)
        territory.owner = self

    def remove_territory(self, territory):
        """ Removes a territory from the player's control """
        self.territories.remove(territory)
        territory.owner = None

    def calculate_armies(self, board):
        # Calculate armies based on territories owned
        armies_from_territories = max(len(self.territories) // 3, 3)

        # Calculate continent bonuses
        continent_bonus = self.calculate_continent_bonus(board)

        return armies_from_territories + continent_bonus

    def calculate_continent_bonus(self, board):
        continent_armies = {
            'Africa': 3, 'Asia': 7, 'Australia': 2, 'Europe': 5, 'North America': 5, 'South America': 2
        }
        bonus = 0
        for continent in board.continents.values():
            if all(territory.owner == self for territory in continent.territories):
                bonus += continent_armies[continent.name]
        return bonus

    def place_armies(self, territory, number):
        """Places a specified number of armies on a territory."""
        if territory in self.territories and number <= self.armies:
            territory.armies += number
            self.armies -= number


    def receive_armies(self, number):
        """ Receives a specified number of armies """
        self.armies += number


    def choose_territory(self, available_territories):
        """ Allows the player to choose a territory from the available ones """
        print("Available territories:")
        for i, territory in enumerate(available_territories):
            print(f"{i + 1}: {territory.name}")

        choice = int(input(f"{self.name}, choose a territory by number: ")) - 1
        # Ensure the choice is valid
        if 0 <= choice < len(available_territories):
            return available_territories[choice]
        else:
            print("Invalid choice. Please choose again.")
            return self.choose_territory(available_territories)

    def place_initial_army(self):
        """ Places initial army player's territories at start of turn """
        while self.armies > 0:
            print(f"{self.name}, you have {self.armies} armies to place.")
            for i, territory in enumerate(self.territories):
                print(f"{i + 1}: {territory.name} (Armies: {territory.armies})")

            try:
                choice = int(input("Choose a territory to place armies: ")) - 1
                if 0 <= choice < len(self.territories):
                    territory = self.territories[choice]
                    armies_to_place = int(input(f"How many armies do you want to place in {territory.name}? "))

                    if 0 < armies_to_place <= self.armies:
                        territory.armies += armies_to_place
                        self.armies -= armies_to_place
                        print(f"Placed {armies_to_place} armies in {territory.name}.")
                    else:
                        print("Invalid number of armies. Please choose a valid number.")
                else:
                    print("Invalid choice. Please choose a valid territory.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def attack(self):
        while True:
            # List attackable territories
            attackable_territories = [t for t in self.territories if t.armies > 1]
            if not attackable_territories:
                print(f"{self.name} has no territories with enough armies to attack.")
                return

            print(f"{self.name}, choose a territory to attack from or type 'exit' to end the attack phase:")
            for i, territory in enumerate(attackable_territories):
                print(f"{i + 1}: {territory.name} (Armies: {territory.armies})")

            from_choice = input("Select a territory to attack from: ")
            if from_choice.lower() == 'exit':
                break

            try:
                from_choice = int(from_choice) - 1
                if 0 <= from_choice < len(attackable_territories):
                    from_territory = attackable_territories[from_choice]

                    # List adjacent territories that can be attacked
                    print("Choose a territory to attack:")
                    attackable_targets = [t for t in from_territory.adjacent_territories if t.owner != self]
                    for i, territory in enumerate(attackable_targets):
                        print(f"{i + 1}: {territory.name} (Armies: {territory.armies})")

                    to_choice = int(input("Select a territory to attack: ")) - 1
                    if 0 <= to_choice < len(attackable_targets):
                        to_territory = attackable_targets[to_choice]

                        # Perform the attack
                        self.perform_attack(from_territory, to_territory)
                    else:
                        print("Invalid choice. Please choose again.")
                else:
                    print("Invalid choice. Please choose again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def perform_attack(self, from_territory, to_territory):
        """ Perform the attack and handle the results """
        while from_territory.armies > 1:
            print(f"{self.name} is attacking {to_territory.name} from {from_territory.name}")
            battle_results = attack(from_territory, to_territory)

            for attacker_roll, defender_roll, outcome in battle_results:
                print(f"Attacker rolled {attacker_roll}, Defender rolled {defender_roll}: {outcome}")

            if to_territory.armies == 0:
                # Territory is conquered
                print(f"{to_territory.name} was conquered!")
                to_territory.owner = self  # Update the ownership
                self.conquered_territory = True
                last_attack_dice_count = determine_dice_count(from_territory.armies, 1)[0]
                self.occupy_territory(from_territory, to_territory, last_attack_dice_count)
                break  # Break after successful occupation

            # Ask if they want to continue attacking
            continue_attack = input("Do you want to continue attacking this territory? (yes/no): ")
            if continue_attack.lower() != 'yes':
                break

    def occupy_territory(self, from_territory, to_territory, last_attack_dice_count):
        """ Allows the player to move armies to a newly conquered territory """
        min_armies_to_move = last_attack_dice_count
        max_armies_to_move = from_territory.armies - 1  # Leave at least one army behind

        print(f"You must move at least {min_armies_to_move} armies to {to_territory.name}, but can move up to {max_armies_to_move}.")
        while True:
            try:
                armies_to_move = int(input(f"Enter the number of armies to move to {to_territory.name}: "))
                if min_armies_to_move <= armies_to_move <= max_armies_to_move:
                    from_territory.armies -= armies_to_move
                    to_territory.armies += armies_to_move
                    print(f"{armies_to_move} armies moved to {to_territory.name}.")
                    break
                else:
                    print(f"Invalid number. You must move between {min_armies_to_move} and {max_armies_to_move} armies.")
            except ValueError:
                print("Please enter a valid number.")

    def fortify(self):
        print(f"{self.name}, choose a territory to move armies from or type 'exit' to end the fortification phase:")

        for i, territory in enumerate(self.territories):
            if territory.armies > 1:  # Only list territories with more than 1 army
                print(f"{i + 1}: {territory.name} (Armies: {territory.armies})")

        from_choice = input("Select a territory to move armies from: ")
        if from_choice.lower() == 'exit':
            return

        try:
            from_choice = int(from_choice) - 1
            if 0 <= from_choice < len(self.territories):
                from_territory = self.territories[from_choice]

                if from_territory.armies <= 1:
                    print(f"Not enough armies in {from_territory.name}. Please choose another territory.")
                    return

                print("Choose an adjacent territory to move armies to:")
                for i, territory in enumerate(from_territory.adjacent_territories):
                    print(f"{i + 1}: {territory.name} (Armies: {territory.armies})")

                to_choice = int(input("Select a territory to fortify: ")) - 1
                if 0 <= to_choice < len(from_territory.adjacent_territories):
                    to_territory = from_territory.adjacent_territories[to_choice]

                    number = int(input(
                        f"How many armies do you want to move from {from_territory.name} to {to_territory.name}? "))
                    if 1 <= number < from_territory.armies:
                        fortify(from_territory, to_territory, number)
                        print(f"Moved {number} armies from {from_territory.name} to {to_territory.name}.")
                    else:
                        print("Invalid number of armies. Please choose again.")
                else:
                    print("Invalid choice. Please choose an adjacent territory.")
            else:
                print("Invalid choice. Please choose again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def add_card(self, card):
        """ Adds a card to the player's hand """
        self.cards.append(card)


    def manage_cards(self):
        """Decides whether to trade in cards for armies."""
        if len(self.cards) >= 6:
            print(f"Player {self.name} has {len(self.cards)} cards and must trade in a set.")
            traded_armies = self.trade_cards()
            self.receive_armies(traded_armies)
            print(f"Player {self.name} receives {traded_armies} armies from trading cards.")
        elif self.can_trade_cards():
            trade_decision = input("Do you want to trade in cards for armies? (yes/no): ")
            if trade_decision.lower() == 'yes':
                traded_armies = self.trade_cards()
                self.receive_armies(traded_armies)
                print(f"Player {self.name} receives {traded_armies} armies from trading cards.")
        else:
            print("You don't have enough cards to trade.")

    def can_trade_cards(self):
        """ Check if the player can trade cards for armies """
        infantry_count = sum(1 for card in self.cards if card.type == "Infantry")
        cavalry_count = sum(1 for card in self.cards if card.type == "Cavalry")
        artillery_count = sum(1 for card in self.cards if card.type == "Artillery")

        # Check for three of the same type
        if infantry_count >= 3 or cavalry_count >= 3 or artillery_count >= 3:
            return True

        # Check for one of each type
        if infantry_count > 0 and cavalry_count > 0 and artillery_count > 0:
            return True

        return False

    def trade_cards(self):
        """ Handles the logic of trading cards for armies """
        if not self.can_trade_cards():
            print("You don't have enough cards to trade.")
            return 0

        # Display cards with numbers
        print("Your cards:")
        for i, card in enumerate(self.cards, 1):
            print(f"{i}: {card.type}")

        # Ask the player to choose cards to trade by number
        card_indices = input("Enter the numbers of the cards to trade (e.g., '1 2 3'): ").split()

        # Convert input to integers and adjust for zero-based index
        try:
            card_indices = [int(index) - 1 for index in card_indices]
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return 0

        # Validate the chosen set
        if self.valid_set_by_indices(card_indices):
            self.remove_cards_by_indices(card_indices)
            traded_armies = self.determine_trade_in_value()
            Player.total_sets_traded += 1
            return traded_armies
        else:
            print("Invalid set of cards. Please try again.")
            return 0

    def valid_set_by_indices(self, indices):
        """ Checks if the chosen set of card indices is valid for trade """
        if len(indices) != 3 or not all(0 <= i < len(self.cards) for i in indices):
            return False

        # Extract card types based on indices
        card_types = [self.cards[i].type for i in indices]
        print(f"Selected card types for trading: {card_types}")  # Debugging print

        # Call valid_set with the card types
        return self.valid_set(card_types)

    def remove_cards_by_indices(self, indices):
        """ Removes cards based on a list of indices """
        for index in sorted(indices, reverse=True):
            del self.cards[index]

    def valid_set(self, card_types):
        """ Checks if the chosen set of cards is valid for trade """
        # Convert the player's cards to a list of their types
        player_card_types = [card.type for card in self.cards]

        # Check if all three cards are the same type
        if card_types[0] == card_types[1] == card_types[2]:
            return player_card_types.count(card_types[0]) >= 3

        # Check if the cards are one of each type
        if set(card_types) == {"Infantry", "Cavalry", "Artillery"}:
            # Ensure the player has at least one of each type in their hand
            return all(card_types.count(card_type) <= player_card_types.count(card_type) for card_type in set(card_types))

        return False

    def remove_cards(self, card_types):
        """ Removes the chosen set of cards from the player's hand """
        for card_type in card_types:
            for card in self.cards:
                if card.type == card_type:
                    self.cards.remove(card)
                    break

    def determine_trade_in_value(self):
        """ Determines the number of armies based on the number of sets traded """
        base_values = [4, 6, 8, 10, 12, 15]  # Base values for the first six sets
        if Player.total_sets_traded < len(base_values):
            return base_values[Player.total_sets_traded]
        else:
            return 15 + 5 * (Player.total_sets_traded - len(base_values) + 1)

    def show_cards(self):
        if not self.cards:
            print("You currently have no cards.")
        else:
            print("Your cards:")
            for card in self.cards:
                print(f"- {card.type}")


