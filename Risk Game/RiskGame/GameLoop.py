from RiskGame.RiskBoard import Board
from RiskGame.Player import Player
from RiskGame.Card import draw_card
from RiskGame.Worldmap import refresh_display
from RiskGame.Mechanics import attack, fortify
from RiskGame.RiskBoard import Continent
from RiskGame.Card import Card
import random

board = Board()
players = Player


def setup_game(num_players):
    board = Board()
    board.initialize_board()

    # Randomly distribute territories among all players, including the PPOAgent
    all_territories = list(board.territories.values())
    random.shuffle(all_territories)
    territories_per_player = len(all_territories) // num_players

    # Create Player instances for human players and add them to the list
    players = [Player(f"Player {i + 1}") for i in range(num_players)]

    # Distribute territories
    for i, territory in enumerate(all_territories):
        player = players[i % num_players]
        player.add_territory(territory)
        territory.armies = 1  # Initial army placement

    # Assign initial armies to all players, including the PPOAgent
    initial_armies = {2: 40, 3: 35, 4: 30, 5: 25, 6: 20}.get(num_players, 20)
    for player in players:
        player_initial_armies = max(initial_armies - len(player.territories), 3)
        player.receive_armies(player_initial_armies)

    return board, players

def receive_armies(player, board):
    # Simplified example: 1 army per 3 territories
    new_armies = max(len(player.territories) // 3, 3)  # Ensure minimum of 3 armies
    if player.can_trade_cards():
        # Additional armies from trading cards (implement based on your game's rules)
        new_armies += 5  # Placeholder value
    player.receive_armies(new_armies)



def check_win_condition(players, board):
    # Player wins when they control all territories
    for player in players:
        if len(player.territories) == len(board.territories):
            return player
    return None


def get_current_state(env):
    # Call the get_observation method of the RiskGameEnv instance
    return env.get_observation()


