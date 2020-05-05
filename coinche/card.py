import numpy as np
from enum import Enum


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __lt__(self, other):
        return self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit)

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        return self.rank > other.rank or (self.rank == other.rank and self.suit > other.suit)

    def __le__(self, other):
        return not (self > other)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.rank.__str__() + self.suit.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def to_index(self, suits_order):
        suit_position = suits_order.index(self.suit)
        rank_position = self.rank.value
        return rank_position + (suit_position * 8)

    @staticmethod
    def from_index(card_index, suits_order):
        card_rank = (card_index % 8)
        card_suit = int(card_index / 8)
        return Card(Rank(card_rank), Suit(suits_order[card_suit]))


class Suit(Enum):
    # Suit identification
    # The suit that leads is trump, aces are high
    CLUB = 0
    DIAMOND = 1
    SPADE = 2
    HEART = 3

    @staticmethod
    def create_order(atout_suit):
        suits_order = np.array(list(Suit))
        while True:
            if suits_order[0] == atout_suit:
                break
            suits_order = np.roll(suits_order, 1)
        return suits_order.tolist()


class Rank(Enum):
    # Ranks indicated
    # Where ace is high and two is low
    SEVEN = 0
    HEIGHT = 1
    NINE = 2
    TEN = 3
    JACK = 4
    QUEEN = 5
    KING = 6
    ACE = 7
