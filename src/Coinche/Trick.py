from .Card import Suit, Card, Rank
# Defining atout_rank, generic_values, atout_values
from .CardsOrder import *
hearts = 3 # the corresponding index to the suit hearts
spades = 2
queen = 12


class Trick:
    def __init__(self):
        self.trick = [Card(0,-1), Card(0,-1), Card(0,-1), Card(0,-1)]
        self.suit = Suit(spades)
        self.cardsInTrick = 0
        self.highest = 0 # rank of the high trump suit card in hand
        self.winner = -1
        self.highest_is_atout = False
        self.highest_rank = 0

    def setTrickSuit(self, card):
        self.suit = card.suit

    def _assert_valid_play(self, add_card, current_player):

        # If suit is atout, you must go higher if you can
        if (add_card is not None and
                add_card.suit == Suit(self.atout_suit) and
                self.currentTrick.suit == Suit(self.atout_suit)):

            if (current_player.hasHigherAtout(self.atout_suit, self.currentTrick.highest_rank) and
                    atout_rank[add_card.rank.rank] < self.currentTrick.highest_rank):
                print("Must put a higher atout")
                add_card = None

            # player tries to play off suit but has trick suit
        if add_card is not None and add_card.suit != self.currentTrick.suit:
            if current_player.hasSuit(self.currentTrick.suit):
                print("Must play the suit of the current trick.")
                add_card = None
            elif current_player.hasAtout(Suit(self.atout_suit)) and add_card.suit != Suit(self.atout_suit):
                print("Must play Atout.")
                add_card = None
            elif (current_player.hasAtout(Suit(self.atout_suit)) and
                  add_card.suit == Suit(self.atout_suit)):
                # Player can play a higher atout but doesn't do so --> forced to play a higher atout
                if (self.currentTrick.highest_is_atout and
                        current_player.hasHigherAtout(self.atout_suit, self.currentTrick.highest_rank) and
                        atout_rank[add_card.rank.rank] < self.currentTrick.highest_rank):
                    print("Must put a higher atout")
                    add_card = None
        return add_card


    # TODO: check compatibility of adding "car" based on current trick + player_hand
    # otherwise raise an exception
    def addCard(self, card, player_hand):
        if self.cardsInTrick == 0: # if this is the first card added, set the trick suit
            self.setTrickSuit(card)
            #print ('Current trick suit:', self.suit)

        self.trick[index] = card
        self.cardsInTrick += 1
        # If the card is an atout
        if card.suit == atout_suit:

            if not self.highest_is_atout:
                self.highest_rank = atout_rank[card.rank.rank]
                self.highest = atout_values[card.rank.rank]
                self.winner = index
                self.highest_is_atout = True

            else:
                if atout_values[card.rank.rank] > self.highest:
                    self.highest_rank = atout_rank[card.rank.rank]
                    self.highest = atout_values[card.rank.rank]
                    self.winner = index
            # Is the atout  better than a previous atout. Comparing Values and than Ranks are the same among a suit or among atouts
        if not self.highest_is_atout:

            if card.suit == self.suit:
                if generic_values[card.rank.rank] > self.highest:
                    self.highest = generic_values[card.rank.rank]
                    self.winner = index
                    #print ("Highest:",self.highest)

