from coinche.Card import Suit, Card, Rank
from coinche.CardsOrder import atout_rank, generic_rank, generic_values, atout_values
from coinche.exceptions import MustPlayHigherAtout, MustPlayACard, MustPlayCurrentSuit, MustPlayAtout, MustPlayHisCards


class Trick:
    def __init__(self, atout_suit, trick_number):
        self.trick = [Card(0, -1), Card(0, -1), Card(0, -1), Card(0, -1)]
        self.atout_suit = atout_suit
        self.trick_number = trick_number
        self.suit = None
        self.cardsInTrick = 0
        self.winner = -1
        self.highest_is_atout = False
        self.highest_rank = 0

    def _assert_valid_play(self, card, player_hand):
        if card is None:
            raise MustPlayACard()

        if not player_hand.hasCard(card):
            raise MustPlayHisCards()

        # player tries to play off suit but has trick suit
        if card.suit != self.suit:
            if player_hand.hasSuit(self.suit):
                raise MustPlayCurrentSuit("Must play the suit of the current trick", self.suit)
            elif card.suit != self.atout_suit and player_hand.hasAtout(self.atout_suit):
                raise MustPlayAtout()
            elif card.suit == self.atout_suit:
                # Player can play a higher atout but doesn't do so --> forced to play a higher atout
                if (self.highest_is_atout and
                        atout_rank[card.rank.rank] < self.highest_rank and
                        player_hand.hasHigherCard(self.atout_suit, atout_rank, self.highest_rank)):
                    raise MustPlayHigherAtout()

        # If suit is atout, you must go higher if you can
        if self.suit == self.atout_suit and card.suit == self.atout_suit:
            if (atout_rank[card.rank.rank] < self.highest_rank and
                    player_hand.hasHigherCard(self.atout_suit, atout_rank, self.highest_rank)):
                raise MustPlayHigherAtout()

    def addCard(self, card, player_hand, player_index):
        if self.cardsInTrick == 0:  # if this is the first card added, set the trick suit
            self.suit = card.suit
        if self.cardsInTrick > 0:
            self._assert_valid_play(card, player_hand)

        self.trick[player_index] = card
        self.cardsInTrick += 1

        # If the card is an atout
        if card.suit == self.atout_suit:
            if not self.highest_is_atout:
                self.highest_rank = atout_rank[card.rank.rank]
                self.winner = player_index
                self.highest_is_atout = True
            else:
                # Is the atout  better than a previous atout.
                if atout_rank[card.rank.rank] > self.highest_rank:
                    self.highest_rank = atout_rank[card.rank.rank]
                    self.winner = player_index
        # Comparing Values and than Ranks are the same among a suit or among atouts
        if not self.highest_is_atout:
            if card.suit == self.suit:
                if generic_rank[card.rank.rank] > self.highest_rank:
                    self.highest_rank = generic_rank[card.rank.rank]
                    self.winner = player_index

    def score(self):
        """
        This function computes the value of the trick given if the cards are atout cards or not
        ex:
        if atout_suit is heart and the trick is [Ad, Td, 9h, 7d]:
        --> the trickValue is 11(Ad) + 10(Td) + 14(9h) + 0(7d) = 35 for player "Sud"

        There is also the 10 de der that gives ten extra points if you win last trick (7th trick)
        """
        trick_value = 0
        for card in self.trick:
            if card != Card(0, -1):
                if card.suit == self.atout_suit:
                    trick_value += atout_values[card.rank.rank]
                else:
                    trick_value += generic_values[card.rank.rank]
        # 10 de der
        if self.trick_number == 8:
            trick_value += 10
        return trick_value

    def is_done(self):
        return self.cardsInTrick >= 4
