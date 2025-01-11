import random
from .card import Card

class Deck:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = [ '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    def __init__(self):
       self.reset()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_hands, num_cards_per_hand):
        hands = []
        for _ in range(num_hands):
            hand = [self.cards.pop() for _ in range(num_cards_per_hand)]
            hands.append(hand)
        return hands
    def reset(self):
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
        self.shuffle()