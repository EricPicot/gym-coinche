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


class UnknownCard(Card):
    def __init__(self):
        super(UnknownCard, self).__init__(-1, -1)


class Suit(Enum):
    # Suit identification
    # The suit that leads is trump, aces are high
    CLUB = 0
    DIAMOND = 1
    SPADE = 2
    HEART = 3


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
