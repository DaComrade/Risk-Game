import random

def roll_dice(number):
    """ Roll a specified number of dice and return the results """
    return sorted([random.randint(1, 6) for _ in range(number)], reverse=True)

def determine_dice_count(attacker_armies, defender_armies):
    attacker_dice = min(3, attacker_armies - 1)  # Attacker must leave 1 army behind
    defender_dice = min(2, defender_armies)      # Defender can roll up to 2 dice
    return attacker_dice, defender_dice

def attack(attacker, defender):
    """ Simulates an attack from one territory to another """

    attacker_dice, defender_dice = determine_dice_count(attacker.armies, defender.armies)
    attacker_rolls = roll_dice(attacker_dice)
    defender_rolls = roll_dice(defender_dice)

    print(f"Attacker Rolls: {attacker_rolls}, Defender Rolls: {defender_rolls}")

    battle_results = []

    # Compare the dice rolls from highest to lowest
    for a_roll, d_roll in zip(attacker_rolls, defender_rolls):
        if a_roll > d_roll:
            defender.armies -= 1
            battle_results.append((a_roll, d_roll, "Attacker wins this round"))
        else:
            attacker.armies -= 1
            battle_results.append((a_roll, d_roll, "Defender wins this round"))

        if attacker.armies <= 1 or defender.armies == 0:
            break

    if defender.armies == 0:
        # Handle territory conquest
        defender.owner.remove_territory(defender)
        attacker.owner.add_territory(defender)
        # Move a number of armies to the conquered territory (to be decided by the player)


    return battle_results

def fortify(origin, destination, number):
    """ Move a certain number of armies from one territory to another """
    if origin.owner == destination.owner and origin.armies > number:
        origin.armies -= number
        destination.armies += number