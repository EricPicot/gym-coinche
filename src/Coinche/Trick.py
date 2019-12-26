from .Card import Suit, Card, Rank

hearts = 3 # the corresponding index to the suit hearts
spades = 2
queen = 12

generic_values =dict(
    [(7,0),
    (8,0),
    (9,0),
    (10,10),
    (11,2),
    (12,3),
    (13,4),
    (14,11)]
)


atout_values = dict(
    [(7,0),
    (8,0),
    (9,14),
    (10,10),
    (11,20),
    (12,3),
    (13,4),
    (14,11)]
)

class Trick:
    def __init__(self):
        self.trick = [Card(0,-1), Card(0,-1), Card(0,-1), Card(0,-1)]
        self.suit = Suit(spades)
        self.cardsInTrick = 0
        self.highest = 0 # rank of the high trump suit card in hand
        self.winner = -1
        self.highest_is_atout = False

    def reset(self):
        self.trick = [Card(0,-1), Card(0,-1), Card(0,-1), Card(0,-1)]
#         self.trick = [0, 0, 0, 0]
        self.suit = -1
        self.cardsInTrick = 0
        self.highest = 0
        self.winner = -1
        self.highest_is_atout = False

    # def cardsInTrick(self):
    #     count = 0
    #     for card in self.trick:
    #         if card is not 0:
    #             count += 1
    #     return count

    def setTrickSuit(self, card):
        self.suit = card.suit

    def addCard(self, card, index, atout_suit):
        if self.cardsInTrick == 0: # if this is the first card added, set the trick suit
            self.setTrickSuit(card)
            #print ('Current trick suit:', self.suit)

        self.trick[index] = card
        self.cardsInTrick += 1
        # If the card is an atout
        if card.suit == atout_suit:

            if not self.highest_is_atout:
                self.highest = atout_values[card.rank.rank]
                self.winner = index
                self.highest_is_atout = True

            else:
                if atout_values[card.rank.rank] > self.highest:
                    self.highest = atout_values[card.rank.rank]
                    self.winner = index
            # Is the atout  better than a previous atout
        if not self.highest_is_atout:

            if card.suit == self.suit:
                if generic_values[card.rank.rank] > self.highest:
                    self.highest = generic_values[card.rank.rank]
                    self.winner = index
                    #print ("Highest:",self.highest)

