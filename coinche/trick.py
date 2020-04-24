from coinche.card import UnknownCard, Rank
from coinche.exceptions import MustPlayHigherAtout, MustPlayACard, MustPlayCurrentSuit, MustPlayAtout, MustPlayHisCards


class Trick:
    def __init__(self, atout_suit, trick_number):
        self.cards = []
        self.atout_suit = atout_suit
        self.trick_number = trick_number
        self.suit = None
        self.cards_in_trick = 0
        self.winner = -1
        self.highest_card = UnknownCard()

    def _assert_valid_play(self, card, player):
        if card is None:
            raise MustPlayACard()

        if not player.has_card(card):
            raise MustPlayHisCards()

        # player tries to play off suit
        if card.suit != self.suit:
            # but has trick suit
            if player.has_suit(self.suit):
                raise MustPlayCurrentSuit("Must play the suit of the current trick", self.suit)
            # he is not playing atout
            elif card.suit != self.atout_suit and player.has_suit(self.atout_suit):
                raise MustPlayAtout()
            elif card.suit == self.atout_suit:
                # Player can play a higher atout but doesn't do so --> forced to play a higher atout
                if (self.highest_is_atout() and _ATOUT_RANK[card.rank] < _ATOUT_RANK[self.highest_card.rank]
                        and self.player_can_go_higher(player)):
                    raise MustPlayHigherAtout()

        # If suit is atout, you must go higher if you can
        if self.suit == self.atout_suit and card.suit == self.atout_suit:
            if _ATOUT_RANK[card.rank] < _ATOUT_RANK[self.highest_card.rank] and self.player_can_go_higher(player):
                raise MustPlayHigherAtout()

    def add_card(self, card, player):
        if self.cards_in_trick == 0:  # if this is the first card added, set the trick suit
            self.suit = card.suit
            self.highest_card = card
            self.winner = player
            self.cards.append(card)
            self.cards_in_trick += 1
        else:
            self._assert_valid_play(card, player)
            self.cards.append(card)
            self.cards_in_trick += 1

            if self.is_player_card_higher_than_highest(card):
                self.highest_card = card
                self.winner = player

    def is_player_card_higher_than_highest(self, player_card):
        # If the card is an atout
        if player_card.suit == self.atout_suit:
            if self.highest_card.suit == self.atout_suit:
                # Is the atout  better than a previous atout.
                return _ATOUT_RANK[player_card.rank] > _ATOUT_RANK[self.highest_card.rank]
            else:
                return True
        # Comparing Values and than Ranks are the same among a suit or among atouts
        else:
            if player_card.suit == self.suit:
                return _GENERIC_RANK[player_card.rank] > _GENERIC_RANK[self.highest_card.rank]
            else:
                return False

    def score(self):
        """
        This function computes the value of the trick given if the cards are atout cards or not
        ex:
        if atout_suit is heart and the trick is [Ad, Td, 9h, 7d]:
        --> the trickValue is 11(Ad) + 10(Td) + 14(9h) + 0(7d) = 35 for player "Sud"

        There is also the 10 de der that gives ten extra points if you win last trick (7th trick)
        """
        trick_value = 0
        for card in self.cards:
            if card != UnknownCard():
                if card.suit == self.atout_suit:
                    trick_value += _ATOUT_VALUES[card.rank]
                else:
                    trick_value += _GENERIC_VALUES[card.rank]
        # 10 de der
        if self.trick_number == 8:
            trick_value += 10
        return trick_value

    def highest_is_atout(self):
        return self.atout_suit == self.highest_card.suit

    def player_can_go_higher(self, player):
        atout_cards = player.get_suit_card(self.atout_suit)
        for card in atout_cards:
            if _ATOUT_RANK[card.rank] > _ATOUT_RANK[self.highest_card.rank]:
                return True
        return False

    def is_done(self):
        return self.cards_in_trick >= 4


_GENERIC_VALUES = dict(
    [(Rank.SEVEN, 0),
     (Rank.HEIGHT, 0),
     (Rank.NINE, 0),
     (Rank.TEN, 10),
     (Rank.JACK, 2),
     (Rank.QUEEN, 3),
     (Rank.KING, 4),
     (Rank.ACE, 11)]
)

_GENERIC_RANK = dict(
    [(Rank.SEVEN, 1),
     (Rank.HEIGHT, 2),
     (Rank.NINE, 3),
     (Rank.TEN, 7),
     (Rank.JACK, 4),
     (Rank.QUEEN, 5),
     (Rank.KING, 6),
     (Rank.ACE, 8)]
)

_ATOUT_VALUES = dict(
    [(Rank.SEVEN, 0),
     (Rank.HEIGHT, 0),
     (Rank.NINE, 14),
     (Rank.TEN, 10),
     (Rank.JACK, 20),
     (Rank.QUEEN, 3),
     (Rank.KING, 4),
     (Rank.ACE, 11)]
)

_ATOUT_RANK = dict(
    [(Rank.SEVEN, 1),
     (Rank.HEIGHT, 2),
     (Rank.NINE, 7),
     (Rank.TEN, 5),
     (Rank.JACK, 8),
     (Rank.QUEEN, 3),
     (Rank.KING, 4),
     (Rank.ACE, 6)]
)
