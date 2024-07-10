import random

class Card:
    def __init__(self, type):
        self.type = type

def draw_card():
    types = ["Infantry", "Cavalry", "Artillery"]
    card_type = random.choice(types)
    print(f"A {card_type} card was drawn.")
    return Card(card_type)