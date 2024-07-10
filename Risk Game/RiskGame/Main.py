import random
import pygame

from RiskGame.RiskBoard import Board
from RiskGame.Player import Player
from RiskGame.GameLoop import setup_game, check_win_condition
from RiskGame.Worldmap import refresh_display, handle_pygame_events, close_pygame
from RiskGame.Card import draw_card

def player_turn(player, board, players):


    print(f"\n{player.name}'s turn:")

    # Step 1: Receive Armies

    armies_to_allocate = player.calculate_armies(board)
    print(f"{player.name} receives {armies_to_allocate} armies.")
    player.armies += armies_to_allocate

    # Human player's turn
    player.place_initial_army()
    board.set_current_phase('placing')
    refresh_display(board)
    player.attack()
    board.set_current_phase('attacking')
    refresh_display(board)
    fortify_decision = input(f"{player.name}, do you want to fortify a position? (yes/no): ")
    board.set_current_phase('fortifying')
    if fortify_decision.lower() == 'yes':
        player.fortify()
        refresh_display(board)
    player.manage_cards()  # Including card trading logic

    # Check for conquered territory for card reward
    if player.conquered_territory:
        player.add_card(draw_card())
        player.conquered_territory = False

    # Optional: Show cards
    show_cards_decision = input(f"{player.name}, do you want to view your cards? (yes/no): ")
    if show_cards_decision.lower() == 'yes':
        player.show_cards()

    player.conquered_territory = False  # Reset the flag

    board.set_current_phase('placing')


def main_game_loop(players, board):
    game_over = False
    while not game_over:
        print("Players list before loop:", [player.name for player in players])
        for player in players:
            print(f"Current player: {type(player).__name__}")  # Log the type of the current player
            player_turn(player, board, players)

            refresh_display(board)

            winner = check_win_condition(players, board)
            if winner:
                print(f"\nGame Over! {winner.name} has won!")
                game_over = True
                break

            if not handle_pygame_events():
                game_over = True
                break

    return game_over


if __name__ == "__main__":
    num_players = 4
    board, players = setup_game(num_players)
    print([type(player).__name__ for player in players])
    game_over = main_game_loop(players, board)

    if game_over:
        print("Game has concluded.")
    else:
        print("Game terminated prematurely.")

    close_pygame()