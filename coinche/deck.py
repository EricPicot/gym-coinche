import random as rand

from coinche.card import Card, Rank, Suit

numSuits = 4
minRank = 7
maxRank = 15


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        rand.shuffle(self.cards, rand.random)

    def deal(self, number_of_cards):
        cards = []
        for i in range(number_of_cards):
            cards += [self.cards.pop(0)]
        return cards

    def size(self):
        return len(self.cards)

    def add_cards(self, cards):
        self.cards += cards
        
    def add_trick(self, trick):
        self.cards += trick.cards
        
    def cut_deck(self):
        # Randomly cuts the deck
        cut = rand.randint(2, len(self.cards)-3)
        self.cards = self.cards[-cut:] + self.cards[0:len(self.cards) - cut]

    def __str__(self):
        deck_str = ''
        for card in self.cards:
            deck_str += card.__str__() + '\n'
        return deck_str
